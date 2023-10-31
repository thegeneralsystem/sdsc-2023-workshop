- [I. High Level Analysis](#i-high-level-analysis)
  - [A. Location popularity](#a-location-popularity)
  - [B. Distribution of customers at locations](#b-distribution-of-customers-at-locations)
  - [C. Visits by time period](#c-visits-by-time-period)
- [II. Cross-visitation](#ii-cross-visitation)
  - [A. Analysing a single customer's behaviour](#a-analysing-a-single-customers-behaviour)
  - [B. Aggregated cross-visitation for all customers](#b-aggregated-cross-visitation-for-all-customers)
- [III. Hotspots in Time](#iii-hotspots-in-time)
- [IV. Customer Journeys](#iv-customer-journeys)

# Mobility Data Analysis

[![Notebook 2 - Mobility Analysis](https://img.shields.io/badge/notebook_2-mobility_analysis-FF5008)](https://mybinder.org/v2/gh/thegeneralsystem/sdsc-2023-workshop/main?labpath=notebooks%2F2_mobility_analysis.ipynb)

```admonish warning title="DFI Queries Will Not Work"
The Data Flow Index server used for this workshop is no longer running.  The workshop materials are left up _as is_ but queries will not run.  If you would like to trial the Data Flow Index please reach out to General System at [https://www.generalsystem.com/contact-us](https://www.generalsystem.com/contact-us).
```

Now we get to look at some data!

## I. High Level Analysis

### A. Location popularity

Let's measure location popularity by viewing the overall number of visits(dwells) each Blank Street Coffee shop received. Callsigns have been assigned to each location to improve readability, these are not real shop names!

```txt
        location_id  dwell_count    callsign
0	101322157	44	    Breve
1	265149230	35	    Coconut Mocha
2	188549793	34	    Macchiato
3	270907009	30	    Turkish
4	278078941	30	    Hazelnut Mocha
```

### B. Distribution of customers at locations

While the number of customers might seem a similar metric to the number of visits, some locations might be visited frequently by a small and loyal set of customers, whereas other locations might be visited once or twice by a large number of customers. This analysis allows for more detailed insights into location performance and customer behaviour.

```python
location_customers = (
    bsc_dwells_df.groupby("location_id")["customer_id"]
    .nunique()
    .reset_index()
    .merge(
        bsc_gdf[["osm_id", "callsign"]],
        left_on="location_id",
        right_on="osm_id",
        how="left",
    )
    .drop("osm_id", axis=1)
    .rename(columns={"customer_id": "customer_count"})
    .sort_values(by="customer_count", ascending=False)
    .reset_index(drop=True)
)
```

<center>
<img
    src="/assets/figures/customers_per_location.svg"
    alt="Customers Per Location"
    style="border-radius:10px"
/>
</center>

### C. Visits by time period

To gain an understanding of customer behaviour, a time period analysis is particularly useful. This could be used, for example, to influence the allocation of staff schedules or timing of goods deliveries.

```python
# Assign each ping its time period
bsc_dwells_df = bsc_dwells_df.assign(
    day_of_week=lambda df: df.start_time.dt.day_name(),
    hour_of_day=lambda df: df.start_time.dt.hour,
)

# Overlay time periods on an empty array to ensure no gaps
all_combinations = pd.MultiIndex.from_product(
    [days_of_week, range(24)], names=["day_of_week", "hour_of_day"]
)
heatmap_df = (
    bsc_dwells_df.groupby(["day_of_week", "hour_of_day"])
    .size()
    .reset_index(name="count")
    .set_index(["day_of_week", "hour_of_day"])
    .reindex(all_combinations)
    .reset_index()
    .fillna(value={"count":0})
)
```

<center>
<img
    src="/assets/figures/heatmap.svg"
    alt="Visits by Day of the Week"
    style="border-radius:10px"
/>
</center>

## II. Cross-visitation

Cross visitation is an examination of the customers' dwell locations: that is, the locations those customers visit aside from Blank Street Coffee. Cross-visitation allows one to make comparitive analyses, which enable us to answer simple questions like:

- What proportion of BSC customers also visit other coffee shops?
- What proportion of BSC customers visit multiple BSC shops?

After some further statistical analysis, more complex questions can be answered:

- Are BSC customers more likely to visit a competitor coffee shop or a BSC coffee shop?
- Are BSC customers more likely to visit a competitor coffee shop or a BSC coffee shop than the general population?
- Do repeat customers frequent only the same BSC shop or do they visit other BSC shops?

### A. Analysing a single customer's behaviour

Below is an interactive map displaying the dwell locations of a single Blank Street Coffee customer. Each location is highlighted by a blue circle for greater visibility, with the opacity varying based on the frequency of dwells at the location. The coffee cup symbols denote Blank Street Coffee shops.

<iframe 
    src="/assets/figures/cross_visitation_map.html" 
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

```python
# Choose a customer
customer = "65b753d2-b523-467f-9c39-bc0fd6e2393b"
customer_dwells_df = agg_df[agg_df["customer_id"]==customer]

# Merge OSM building data onto dataframe to get information about other locations
cd_df = merge_osm_data(customer_dwells_df, osm_gdf)
location_dwell_count = pd.DataFrame(cd_df["label"].value_counts().reset_index())
```

The user defined function `merge_osm_data` performs a left join, merging the OSM data geodataframe onto the dwells dataframe, using the "location_id" columns as the primary key. Additionally, it creates a "label" column which concatenates the OSM building metadata to improve readability.

<center>
<img
    src="/assets/figures/dwells_per_location.svg"
    alt="Dwells per Location"
    style="border-radius:10px"
/>
</center>

_Note: This chart is interactive. Hovering your mouse over a bar will display the exact number. Additionally, this chart only represents locations with names or categories assigned to them._

### B. Aggregated cross-visitation for all customers

Using the same function, we can merge the OSM data with the dwells data and find the most popular places visited by the customers. If the data were real, one could use this analysis to gain insights into the most common preferences and interests of the customers.

```python
agg_cd_df = merge_osm_data(agg_df, osm_gdf)
```

<center>
<iframe 
    src="/assets/figures/cross_visitation.html" 
    style="border:0px #ffffff none; border-radius: 10px;" 
    name="20 Most Popular Buildings" 
    scrolling="yes" 
    frameborder="1"
    marginheight="10px" 
    marginwidth="10px" 
    height="360px" 
    width="500px" 
    allowfullscreen> 
</iframe>
</center>

_Note: This chart is interactive. Hovering your mouse over a bar will display the total time (hours) spent dwelling at this location._

## III. Hotspots in Time

Viewing trends in the data through the lens of a time period breakdown can provide a useful visual aid, or a simple answer to a general query.

What if we wanted to find out where customers most commonly visited at 12pm on a Wednesday?

- Aggregating by the day and hour columns, we can count the most common label value, and how many times it occured within the day/hour group.
- After a bit of tidying, and reindexing the time period breakdown onto a grid of all combinations, another heat map can be generated to show the most visited location at any given hour of any given day.

The resulting chart contains 1 year's worth of customer behaviour grouped by day of the week and hour of day; this is not a projection of a single week of the year.

<iframe 
    src="/assets/figures/time_period_heatmap.html" 
    style="border:0px #ffffff none; border-radius: 10px;" 
    name="Customers per BSC Location" 
    scrolling="yes" 
    frameborder="1" 
    marginheight="10px" 
    marginwidth="10px" 
    height="230px" 
    width="720px" 
    allowfullscreen> 
</iframe>

_Note: This chart is interactive. Hovering your mouse over a cell will show you the location information._

## IV. Customer Journeys

“Which other businesses did my customers visit, immediately before they visited me?”

In this example we will use the same customer as before. We will view their dwell history and build a list of locations they visited immediately before and after their visits to Blank Street Coffee shops.

The method of this analysis is:

- Filter dwells for Blank Street Coffee shop dwells

```python
results = []
final_dwell = customer_dwells_df.index.max()
bsc_dwells_df = customer_dwells_df[customer_dwells_df["location_id"].isin(bsc_osm_ids)]
```

- For each location:

```python
for bsc_location in bsc_dwells_df["location_id"]:
```

- Find which dwells are at the location

```python
  bsc_dwell_indexes = customer_dwells_df[
      customer_dwells_df["location_id"] == bsc_location
  ].index.unique()
```

- Loop through dwells to find previous and next dwells

```python
  for index in bsc_dwell_indexes:

      row = {"bsc_location": bsc_location}
      if index != final_dwell:
          row["next_location"] = customer_dwells_df[
              customer_dwells_df.index == index + 1
          ]["location_id"].unique()[0]
      else:
          row["next_location"] = None

      if index != 0:
          row["previous_location"] = customer_dwells_df[
              customer_dwells_df.index == index - 1
          ]["location_id"].unique()[0]
      else:
          row["previous_location"] = None
      results.append(row)
```

- Create a dataframe with the results and group by location

```python
results_df = pd.DataFrame.from_records(results)
results_df.groupby("bsc_location")[["previous_location","next_location"]].value_counts()
```

|     | previous_location | bsc_location      | next_location     | count |
| --: | :---------------- | :---------------- | :---------------- | ----: |
|   0 | id_248298838      | BSC - Dirty Chai  | id_248274214      |     1 |
|   1 | BSC - Kopi Tubruk | BSC - Kopi Tubruk | BSC - Kopi Tubruk |     8 |
|   2 | BSC - Kopi Tubruk | BSC - Kopi Tubruk | id_282925839      |     4 |
|   3 | id_248274214      | BSC - Kopi Tubruk | BSC - Kopi Tubruk |     4 |
