# Switch to 'sdsc-2023-workshop/scripts' directory to run

import base64
import shutil
from pathlib import Path

import geopandas as gpd
import pydeck as pdk
import urllib3

# <a href="https://www.flaticon.com/free-icons/coffee" title="coffee icons">Coffee icons created by Good Ware - Flaticon</a>
COFFEE_CUP_ICON = "../presentation/src/assets/images/cup.png"
BSC_LOGO_COLOR = [103, 150, 113]


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


def main() -> None:
    bsc_gdf = load_location_data(
        "bsc_gdf", "https://d3ftlhu7xfb8rb.cloudfront.net/blank_street_coffee_callsigns.geoparquet"
    )

    centroids = bsc_gdf.geometry.centroid
    bsc_gdf = bsc_gdf.assign(center=list(zip(centroids.x, centroids.y)), longitude=centroids.x, latitude=centroids.y)

    view = pdk.data_utils.compute_view(bsc_gdf.center)

    bsc_layer = pdk.Layer(
        "GeoJsonLayer",
        bsc_gdf,
        opacity=0.5,
        pickable=True,
        stroked=True,
        filled=True,
        get_fill_color=BSC_LOGO_COLOR,
        get_line_color=BSC_LOGO_COLOR,
    )

    map_marker_url = load_local_image_as_data_url(COFFEE_CUP_ICON)
    icon_data = {"width": 80, "height": 80, "url": map_marker_url, "mask": True}

    bsc_gdf = bsc_gdf.assign(icon=lambda df: [icon_data] * len(df))

    bsc_icon_layer = pdk.Layer(
        "IconLayer",
        bsc_gdf,
        get_icon="icon",
        get_position=["longitude", "latitude"],
        get_size=4,
        size_scale=10,
        opacity=0.5,
        get_color=BSC_LOGO_COLOR,
        pickable=True,
        auto_highlight=True,
    )

    r = pdk.Deck(
        layers=[bsc_layer, bsc_icon_layer],
        initial_view_state=view,
        tooltip={
            "html": "<b>Name:</b> {name} <br/> <b>Location:</b> {location} <br/> <b>OSM ID:</b> {osm_id}",
            "style": {"backgroundColor": "#679671", "color": "white", "font-family": "Arial"},
        },
    )

    r.to_html("bsc_map.html")


if __name__ == "__main__":
    main()
