# Identifying BSC Customers

[![Notebook 1 - Identifying BSC Customers](https://img.shields.io/badge/notebook_1-identifying_bsc_customers-FF5008)](https://mybinder.org/v2/gh/thegeneralsystem/sdsc-2023-workshop/main?labpath=notebooks%2F1_identifying_bsc_customers.ipynb/HEAD)

```admonish warning title="DFI Queries Will Not Work"
The Data Flow Index server used for this workshop is no longer running.  The workshop materials are left up _as is_ but queries will not run.  If you would like to trial the Data Flow Index please reach out to General System at [https://www.generalsystem.com/contact-us](https://www.generalsystem.com/contact-us).
```

We say an entity is a customer of BSC if it has dwelled at one or more BSC cafes. To identify the customers in the dataset we query the BSC building polygons for records within each and identify the unique IDs. Since we want to identify just the entities that dwelled at the locations and not ones that just pass by, we need to pull all the records for each entity and calculate their dwells. Here, since the data was synthetically generated, each record is labelled if it is `dwelling`, `walking`, `cycling`, or `driving`. Once we've queried for the entitie's records, we simply filter for those with the `dwelling` label.

```admonish tip
Additional information about each record is stored as a JSON string within each record's `payload` field.
```

```admonish note
This notebook is set to run for a single (or few) devices, but can be amended to run for all Blank Street Coffee customers. This can be done by removing the "break" lines in the dfi query code chunks.
```

## I. Identifying Devices with Data within BSC Locations

- Step 1: Find a list of devices which have pings within Blank Street Coffee locations

```python
bsc_entities: Set[str] = set([])
for _, row in tqdm(bsc_gdf.iterrows(), total=len(bsc_gdf)):
    entities = dfi.get.entities(
        polygon=list(row.geometry.exterior.coords),
    )
    bsc_entities = bsc_entities.union(entities)
    break  # Remove or comment out to run for all entities
```

- Step 2: Retrieve all records for devices

```python
def unpack_payload(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["payload"].apply(lambda x: isinstance(x, str))] # filter out any problem payloads
    df["route"] = df["payload"].apply(lambda x: json.loads(x)["route"])
    df["transportation_mode"] = df["payload"].apply(lambda x: json.loads(x)["transportation_mode"])
    df["start_location_id"] = df["payload"].apply(lambda x: json.loads(x)["start_location_id"])
    df["end_location_id"] = df["payload"].apply(lambda x: json.loads(x)["end_location_id"])

    return df

records_df = dfi.get.records(bsc_entities, add_payload_as_json=True)
records_df = unpack_payload(records_df)
```

- Step 3: Filter this data to find devices which dwelled in Blank Street Coffee locations and get only their records

```python
bsc_gdf = load_location_data(
    "bsc_gdf", "https://d3ftlhu7xfb8rb.cloudfront.net/blank_street_coffee_callsigns.geoparquet"
)
bsc_osm_ids = bsc_gdf["osm_id"]
```

```python
records_df = (
    records_df[records_df["start_location_id"].isin(bsc_osm_ids)
    & records_df["transportation_mode"] == "dwelling"]
)
customers = records_df["entity_id"].unique()
```
