# Intro to Data Flow Index Python API

[![Notebook 0 - Getting Started With DFI](https://img.shields.io/badge/notebook_0-getting_started_with_dfi-FF5008)](https://mybinder.org/v2/gh/thegeneralsystem/sdsc-2023-workshop/main?labpath=notebooks%2F0_getting_started_with_dfi.ipynb)

```admonish warning title="DFI Queries Will Not Work"
The Data Flow Index server used for this workshop is no longer running.  The workshop materials are left up _as is_ but queries will not run.  If you would like to trial the Data Flow Index please reach out to General System at [https://www.generalsystem.com/contact-us](https://www.generalsystem.com/contact-us).
```

There are three main entry points for querying the DFI:

- `dfi.get.records()` - queries for records within the filter bounds
- `dfi.get.entities()` - queries for the unique entities within the filter bounds
- `dfi.get.records_count()` - queries for the count of records within the filter bounds

All three methods have the filter bounds `polygon` and `time_interval`. The `dfi.get.records()` and `dfi.get.records_count()` have an additional filter bound, `entities`.

|          | BBox | Polygon | Entities | Time Interval |
| -------- | ---- | ------- | -------- | ------------- |
| Count    | ✔︎   | ✔︎      | ✔︎       | ✔︎            |
| Entities | ✔︎   | ✔︎      | X        | ✔︎            |
| Records  | ✔︎   | ✔︎      | ✔︎       | ✔︎            |

```admonish info
These filter bounds are optional but at least one filter bound must be specified.
```

```admonish caution
More restrictive filter bounds will result in a more targeted query, whereas a query with less restrictive filter bounds will result in a broader query and may return a larger result set (dependent on the distribution of the dataset).

Running `dfi.get.records()` with loose filter bounds may query for a large number of records. Ensure your machine has enough free memory to collect the query.
```

## I. Workshop Location

```python
def load_location_data(filename: str, url: str) -> gpd.GeoDataFrame:
    """ "Downloads the file at url and saves to a file called filename, returns gdf
    e.g. url = "https://d3ftlhu7xfb8rb.cloudfront.net/blank_street_coffees_callsigns.geoparquet"
    """
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    http = urllib3.PoolManager()
    with open(filename, "wb") as out:
        r = http.request("GET", url, preload_content=False)
        shutil.copyfileobj(r, out)

    return gpd.read_parquet(filename)

gdf = load_location_data("./temp-data", "https://d3ftlhu7xfb8rb.cloudfront.net/london_nyc_osm.geoparquet")

coord = Point(-73.98559984577399,40.75335544582035)

building = gdf[gdf.intersects(coord)]
vertices = [(lon, lat) for lon, lat in building.geometry.iloc[0].exterior.coords]
```

<iframe 
    src="/assets/figures/workshop_location_map.html" 
    style="border:0px #ffffff none; border-radius: 10px;" 
    name="Workshop Location" 
    scrolling="no" 
    frameborder="1" 
    marginheight="0px" 
    marginwidth="0px" 
    height="600px" 
    width="800px" 
    allowfullscreen> 
</iframe>

## II. Querying with Data Flow Index

### A. Initialization

```python
token = "<token>"
instance = "sdsc-2-2088"  # sdsc-1-5148
namespace = "gs"
url = "https://api.prod.generalsystem.com"

dfi = Client(token, instance, namespace, url, progress_bar=True)
```

### B. Count of Records within a Polygon

```python
vertices = [(lon, lat) for lon, lat in building.geometry.iloc[0].exterior.coords]

dfi.get.records_count(
    polygon=vertices,
)
```

```txt
5084
```

### C. Unique IDs within a Polygon

```python
entities = dfi.get.entities(
    polygon=vertices,
)
len(entities)
```

```txt
85
```

### D. Records within a Polygon & Time Interval

```python
start_time = datetime(2022, 1, 1, 0, 0, 0)
end_time = datetime(2022, 2, 1, 1, 0, 0)

df = dfi.get.records(
    polygon=vertices,
    time_interval=(start_time, end_time)
)

df.info()
```

```txt
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 908 entries, 0 to 907
Data columns (total 5 columns):
 #   Column     Non-Null Count  Dtype
---  ------     --------------  -----
 0   entity_id  908 non-null    object
 1   timestamp  908 non-null    datetime64[ns]
 2   longitude  908 non-null    float64
 3   latitude   908 non-null    float64
 4   payload    908 non-null    object
dtypes: datetime64[ns](1), float64(2), object(2)
memory usage: 35.6+ KB
```

### E. Records for an Entity

```python
df = (
    dfi.get.records(entities=["d8084540-f249-4856-ad0d-f6e71fcc545a"], add_payload_as_json=True)
    .assign(payload=lambda df: df.payload.map(json.loads))
)
df = df.join(pd.DataFrame(df.pop("payload").tolist()))

df.head()
```

```txt
entity_id 	timestamp 	longitude 	latitude 	route 	transportation_mode 	start_location_id 	end_location_id
0 	ba64395a-1268-4f90-9197-b9de3aebbc80 	2022-03-13 05:54:30 	-74.092030 	40.599092 	221 	dwelling 	284488890 	284488890
1 	ba64395a-1268-4f90-9197-b9de3aebbc80 	2022-03-13 05:54:56 	-74.092017 	40.599263 	221 	dwelling 	284488890 	284488890
2 	ba64395a-1268-4f90-9197-b9de3aebbc80 	2022-03-13 05:56:06 	-74.091884 	40.598893 	221 	dwelling 	284488890 	284488890
3 	ba64395a-1268-4f90-9197-b9de3aebbc80 	2022-03-13 05:56:30 	-74.092124 	40.599112 	221 	dwelling 	284488890 	284488890
4 	ba64395a-1268-4f90-9197-b9de3aebbc80 	2022-03-13 05:56:35 	-74.091873 	40.599097 	221 	dwelling 	284488890 	284488890
```

$notes$
Audience Questions:

- Who regularly works with Pandas / GeoPandas?
- Is this a familiar workflow?

$notes-end$
