---
title: "Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries"
description: "Comprehensive guide to geospatial data with PostGIS. Understand geometry vs geography types, spatial indexes, and common geospatial queries for GIS applications."
date: 2026-04-06
board: database
url: https://dingjiu1989-hue.github.io/en/database/geospatial-data.html
---

# Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries

Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries 

PostGIS transforms PostgreSQL into a full-featured spatial database. It adds support for geographic objects, spatial indexing, and hundreds of spatial functions. This article covers fundamental concepts and practical query patterns. 

Setting Up PostGIS 

CREATE EXTENSION postgis;

CREATE EXTENSION postgis_topology;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Verify installation

SELECT postgis_version();

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 3.4.0 or similar

Geometry vs Geography 

The most important design decision in PostGIS is choosing between the `geometry` and `geography` data types. 

**Geometry** treats coordinates as Cartesian points on a flat plane. It is appropriate for: 

  * Local datasets where Earth curvature is negligible.

  * Data in projected coordinate systems (UTM, State Plane).

  * Operations that require planar spatial functions.




CREATE TABLE buildings (

id BIGSERIAL PRIMARY KEY,

name TEXT,

location GEOMETRY(Point, 4326), -- SRID 4326 = WGS84 lon/lat

footprint GEOMETRY(Polygon, 4326)

);

INSERT INTO buildings (name, location) VALUES

('City Hall', ST_SetSRID(ST_MakePoint(-73.9857, 40.7484), 4326));

**Geography** treats coordinates on a sphere (or spheroid). It accounts for Earth curvature, making it appropriate for: 

  * Global datasets spanning large distances.

  * Accurate distance calculations in degrees.

  * Queries like "find all points within 10 km."




CREATE TABLE pois (

id BIGSERIAL PRIMARY KEY,

name TEXT,

location GEOGRAPHY(Point, 4326)

);

INSERT INTO pois (name, location) VALUES

('Statue of Liberty', ST_SetSRID(ST_MakePoint(-74.0445, 40.6892), 4326));

**Performance note** : Geography calculations are 2-3x slower than geometry because they use more complex spherical math. For local datasets, cast geography to geometry when precision is not critical. 

Spatial Indexes 

PostGIS uses GiST (Generalized Search Tree) indexes for spatial data: 

CREATE INDEX idx_buildings_location ON buildings USING GIST (location);

CREATE INDEX idx_pois_location ON pois USING GIST (location);

GiST indexes enable indexed spatial operators: `ST_DWithin`, `ST_Intersects`, `ST_Contains`, `ST_Within`, and bounding box comparisons. 

Common Spatial Queries 

Distance Queries 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Find all POIs within 1000 meters of a point

SELECT name, ST_Distance(location, ST_SetSRID(ST_MakePoint(-74.006, 40.7128), 4326)) AS dist_meters

FROM pois

WHERE ST_DWithin(location, ST_SetSRID(ST_MakePoint(-74.006, 40.7128), 4326), 1000)

ORDER BY dist_meters;

`ST_DWithin` uses the index and is far faster than filtering by `ST_Distance` in a WHERE clause. 

Spatial Joins 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Find all buildings within each neighborhood

SELECT n.name AS neighborhood, COUNT(b.id) AS building_count

FROM neighborhoods n

JOIN buildings b ON ST_Contains(n.geom, b.location)

GROUP BY n.name

ORDER BY building_count DESC;

Area Calculations 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Calculate building footprint areas in square meters

SELECT name, ST_Area(footprint::geography) AS area_sqm

FROM buildings

ORDER BY area_sqm DESC;

Nearest Neighbor Search 

The `<->` operator enables efficient nearest-neighbor searches using the GiST index: 

SELECT name, location,

location <-> ST_SetSRID(ST_MakePoint(-73.9857, 40.7484), 4326) AS dist

FROM buildings

ORDER BY location <-> ST_SetSRID(ST_MakePoint(-73.9857, 40.7484), 4326)

LIMIT 5;

Data Import and Export 

Importing GeoJSON 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Cast GeoJSON to geometry

INSERT INTO pois (name, location)

SELECT

properties ->> 'name',

ST_SetSRID(ST_GeomFromGeoJSON(properties ->> 'location'), 4326)

FROM jsonb_array_elements('...geojson array...') AS features;

Importing Shapefiles 

shp2pgsql -s 4326 -I -g geom neighborhoods.shp public.neighborhoods | psql -d mydb

Exporting as GeoJSON 

SELECT row_to_json(fc) AS geojson

FROM (

SELECT

'FeatureCollection' AS type,

json_agg(f) AS features

FROM (

SELECT

'Feature' AS type,

ST_AsGeoJSON(location)::jsonb AS geometry,

jsonb_build_object('name', name) AS properties

FROM pois

) AS f

) AS fc;

Common Spatial Functions 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Transform between coordinate systems

SELECT ST_Transform(location, 3857) FROM buildings; -- to Web Mercator

SELECT ST_Transform(location, 32618) FROM buildings; -- to UTM zone 18N

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Simplify geometry for map display

SELECT ST_Simplify(footprint, 1.0) FROM buildings; -- 1.0 threshold

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Buffer around a point

SELECT ST_Buffer(location::geography, 500) AS five_hundred_m_buffer FROM pois;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Compute convex hull

SELECT ST_ConvexHull(ST_Collect(location)) FROM pois;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Intersection of two geometries

SELECT ST_Intersection(n.geom, b.footprint)

FROM neighborhoods n, buildings b

WHERE ST_Intersects(n.geom, b.footprint);

Performance Optimization 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Cluster a table on its spatial index for faster range scans

CLUSTER buildings USING idx_buildings_location;

ANALYZE buildings;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Use ST_Subdivide for very large geometries

CREATE TABLE neighborhoods_subdivided AS

SELECT id, name,

ST_SubDivide(geom, 200) AS geom

FROM neighborhoods;

CREATE INDEX idx_neighborhoods_subdivided ON neighborhoods_subdivided USING GIST (geom);

PostGIS vs Other Tools 

| Feature | PostGIS | MongoDB 2dsphere | Elasticsearch Geo | |---------|---------|------------------|-------------------| | CRS support | 5000+ SRIDs | WGS84 only | WGS84 only | | Spatial functions | 400+ | 30+ | 20+ | | Topology | Full support | None | None | | Raster support | Yes (PostGIS raster) | No | No | | Routing | pgRouting extension | No | No | 

PostGIS is the most complete open-source spatial database. Use it as the system of record for all geospatial data, and only replicate to specialized tools (map rendering engines, geocoding services) when necessary. Start with geography types for global datasets and geometry for local projections, and always verify index usage in EXPLAIN plans for spatial queries.

**See also:** [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>), [JSON in PostgreSQL: JSONB vs JSON, Indexing, and Operations](</en/database/json-in-postgresql.html>), [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>).

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>)

**See also:** [Database Index Types: B-tree, Hash, GiST, GIN, SP-GiST, BRIN](</en/database/index-types.html>), [Database Connection Management: Pooling, PgBouncer, HikariCP, and Tuning](</en/database/connection-management.html>), [Couchbase Guide: N1QL, Document Model, Clustering, and Caching](</en/database/couchbase-guide.html>)

**See also:** [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [Time-Series with PostgreSQL: TimescaleDB, Hypertables, and Aggregates](</en/database/time-series-postgresql.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)
