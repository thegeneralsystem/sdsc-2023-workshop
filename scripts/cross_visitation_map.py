# Switch to 'sdsc-2023-workshop/scripts' directory to run
import os
import base64
import shutil
from pathlib import Path

import pandas as pd
import geopandas as gpd
import pydeck as pdk
import urllib3

# <a href="https://www.flaticon.com/free-icons/coffee" title="coffee icons">Coffee icons created by Good Ware - Flaticon</a>
COFFEE_CUP_ICON = "../presentation/src/assets/images/cup.png"
BSC_LOGO_COLOR = [103, 150, 113]

# <a href="https://www.flaticon.com/free-icons/dot" title="dot icons">Dot icons created by hirschwolf - Flaticon</a>
CIRCLE_ICON = "../presentation/src/assets/images/circle128px.png"


def load_location_data(filename: str, url: str) -> gpd.GeoDataFrame:
    """ "Downloads the file at url and saves to a file called filename, returns gdf
    e.g. url = "https://d3ftlhu7xfb8rb.cloudfront.net/blank_street_coffees.geoparquet"
    """
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    http = urllib3.PoolManager()
    with open(filename, "wb") as out:
        r = http.request("GET", url, preload_content=False)
        shutil.copyfileobj(r, out)

    return gpd.read_parquet(filename)


def load_local_image_as_data_url(path: str) -> str:
    """Loads and converts a local icon (png image) into a data URL
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs
    """
    return (b"data:image/png;base64," + base64.b64encode(open(path, "rb").read())).decode("ascii")


def custom_color_scale_red(row: pd.Series, df: pd.DataFrame, column: pd.Series) -> list:
    """
    Defines a method to calculate a color (RGBA) based on the value of a column
    """
    normalized_value = (row - df[column].min()) / (df[column].max() - df[column].min())
    # Interpolate color from #FFC6B4 to #FF5722
    color_r = int(255 - (90 * normalized_value))
    color_g = int(198 - (122 * normalized_value))
    color_b = int(180 - (178 * normalized_value))
    # Set alpha to 255 (completely opaque)
    alpha = 255
    return [color_r, color_g, color_b, alpha]


def custom_color_scale_blue(row: pd.Series, df: pd.DataFrame, column: pd.Series) -> list:
    normalized_value = (row - df[column].min()) / (df[column].max() - df[column].min())
    # Interpolate color from #03A9F4 to #9C27B0
    color_r = int(3)
    color_g = int(169)
    color_b = int(244)
    alpha = int(100 + (255 * normalized_value))
    return [color_r, color_g, color_b, alpha]


def main() -> None:
    file_path = "./bsc_gdf"
    if os.path.exists(file_path):
        print("bsc_gdf exists")
        with open(file_path, "rb") as file:
            bsc_gdf = gpd.read_parquet(file_path)
    else:
        print("Reading BSC data")
        bsc_gdf = load_location_data(
            "bsc_gdf", "https://d3ftlhu7xfb8rb.cloudfront.net/blank_street_coffee_callsigns.geoparquet"
        )

    file_path = "./osm_gdf"
    if os.path.exists(file_path):
        print("osm_gdf exists")
        with open(file_path, "rb") as file:
            osm_gdf = gpd.read_parquet(file_path)
    else:
        print("Reading OSM data")
        osm_gdf = load_location_data("osm_gdf", "https://d3ftlhu7xfb8rb.cloudfront.net/london_nyc_osm.geoparquet")

    # Load in customer data
    records_df = pd.read_parquet("https://d3ftlhu7xfb8rb.cloudfront.net/mobility-analysis-input-merged.parquet").rename(
        columns={"uuid": "customer_id"}
    )

    # Create dataframe
    map_pings = records_df[records_df["customer_id"] == "65b753d2-b523-467f-9c39-bc0fd6e2393b"]
    map_of_dwells = (
        map_pings[map_pings["transportation_mode"] == "dwelling"]
        .drop_duplicates("route", keep="first")
        .groupby(by="start_location_id")
        .agg(frequency=("start_location_id", "count"))
        .reset_index()
        .merge(
            osm_gdf[["osm_id", "name", "category", "geometry"]],
            left_on="start_location_id",
            right_on="osm_id",
            how="inner",
        )
        .sort_values(by="frequency", ascending=False)
        .reset_index(drop=True)
    )
    map_of_dwells_gdf = gpd.GeoDataFrame(map_of_dwells, geometry="geometry")
    print(map_of_dwells_gdf[~map_of_dwells_gdf["category"].isna()])
    # Apply the custom_color_scale functions to the "frequency" column
    map_of_dwells_gdf["red_color"] = map_of_dwells_gdf["frequency"].apply(
        custom_color_scale_red, df=map_of_dwells_gdf, column="frequency"
    )

    map_of_dwells_gdf["blue_color"] = map_of_dwells_gdf["frequency"].apply(
        custom_color_scale_blue, df=map_of_dwells_gdf, column="frequency"
    )

    # pydeck code
    centroids = bsc_gdf.geometry.centroid
    bsc_gdf = bsc_gdf.assign(center=list(zip(centroids.x, centroids.y)), longitude=centroids.x, latitude=centroids.y)

    centroids = map_of_dwells_gdf.geometry.centroid
    map_of_dwells_gdf = map_of_dwells_gdf.assign(
        center=list(zip(centroids.x, centroids.y)),
        longitude=centroids.x,
        latitude=centroids.y,
    )

    polygon_layer = pdk.Layer(
        "PolygonLayer",
        data=map_of_dwells_gdf,
        pickable=True,
        stroked=False,
        filled=True,
        get_polygon="geometry.coordinates",
        get_fill_color="red_color",
    )

    map_marker_url = load_local_image_as_data_url(CIRCLE_ICON)
    icon_data = {"width": 80, "height": 80, "url": map_marker_url, "mask": True}

    map_of_dwells_gdf = map_of_dwells_gdf.assign(icon=lambda df: [icon_data] * len(df))
    circle_icon_layer = pdk.Layer(
        "IconLayer",
        map_of_dwells_gdf,
        get_icon="icon",
        get_position=["longitude", "latitude"],
        get_size=3,
        size_scale=10,
        opacity=0.8,
        get_color="blue_color",
        pickable=True,
        auto_highlight=True,
    )

    map_marker_url = load_local_image_as_data_url(COFFEE_CUP_ICON)
    icon_data = {"width": 80, "height": 80, "url": map_marker_url, "mask": True}

    def assign_icon(row):
        if row["osm_id"] in map_of_dwells_gdf["start_location_id"].values:
            return icon_data
        else:
            return None

    bsc_gdf["icon"] = bsc_gdf.apply(assign_icon, axis=1)
    bsc_gdf = bsc_gdf[bsc_gdf["icon"].notnull()]

    bsc_icon_layer = pdk.Layer(
        "IconLayer",
        bsc_gdf,
        get_icon="icon",
        get_position=["longitude", "latitude"],
        get_size=10,
        size_scale=10,
        opacity=1,
        get_color=BSC_LOGO_COLOR,
        pickable=True,
        auto_highlight=True,
    )

    view = pdk.data_utils.compute_view(map_of_dwells_gdf.center)

    # render
    r = pdk.Deck(
        layers=[polygon_layer, bsc_icon_layer, circle_icon_layer],
        initial_view_state=view,
        tooltip={
            "html": "<b>Name:</b> {name} <br/> <b>Category:</b> {category} <br/> <b>OSM ID:</b> {osm_id} <br/> <b>Number of Visits:</b> {frequency}",
            "style": {
                "backgroundColor": "#679671",
                "color": "white",
                "font-family": "Arial",
            },
        },
    )

    r.to_html("../presentation/src/assets/figures/cross_visitation_map.html")


if __name__ == "__main__":
    main()
