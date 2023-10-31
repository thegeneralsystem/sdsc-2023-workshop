# Multiattribute Indexes

_But what if we're working with spatiotemporal data models?_

Geospatial data lives in the real world and thus has not only a spatial element but also a temporal element. Location datasets can be modelled as static in time even though they are updated frequently. Human mobility, GPS, Satellite images, LiDAR, and climate data models are examples of multiattribute data models.

- Traditional indexes do not scale well as datasets grow in size.
- Spatial indexes that discretize space (H3, S3, GeoHash, Quadbins, MGRS) make working with spatial data remarkably simple by projecting into a single dimension. They trade accuracy for simplicity.
- Spatial indexes address geospatial queries but not temporal queries, combinations of the two, nor queries on other dimensions.

## Examples

**Human Mobility:**

`[id, timestamp, latitude, longitude]`

**GPS:**

`[id, timestamp, latitude, longitude, altitude]`

**LiDAR:**

`[id, timestamp, latitude, longitude, altitude]`

**Satellite Image:**

`[id, timestamp, latitude, longitude, altitude, band_1, band_2, band_3, band_4]`

**Climate:**

`[id, timestamp, latitude, longitude, altitude, temperature, humidity, pressure, wind, ux_index]`

$notes$
Aurdience Questions:

- Show of hands, how many people here work with multiattribute data? Multidimensional?

$notes-end$
