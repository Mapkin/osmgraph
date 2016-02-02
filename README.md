osmgraph
========

Create [networkx](https://networkx.github.io/) graphs from OpenStreetMap (OSM)
data.  `osmgraph` uses
[imposm-parser](https://github.com/omniscale/imposm-parser) for parsing
OpenStreetMap XML (including bz2) and PBF
files and [osmqa-parser](https://github.com/mapkin/osmqa-parser) for parsing
[OSM QA tiles](http://osmlab.github.io/osm-qa-tiles/).


Usage
-----

```
>>> import osmgraph
>>> g = osmgraph.parse_file(filename)
```


Graph Structure
---------------
`osmgraph` parses OSM data to create a networkx [directed graph](https://networkx.readthedocs.org/en/stable/reference/classes.digraph.html). OSM nodes correspond directly to the nodes in the directed graph. The OSM tags become attributes of the node. Additionally `osmgraph` adds a `coordinate` attribute containing the (lon, lat) tuple of the node's coordinates.

For example:
```
>>> g = osmgraph.parse_file('boston_massachusetts.osm.bz2')
```

Given the following XML node:
```
  <node id="665539692" lat="42.3971185" lon="-71.0207486" version="2" timestamp="2014-06-25T04:45:25Z" changeset="23135192" uid="422979" user="Parcanman">
    <tag k="railway" v="level_crossing"/>
  </node>
```

```
>>> g.node[665539692]
{'coordinate': (-71.0207486, 42.3971185), 'railway': 'level_crossing'}
```

Similarly, the nodes comprising an OSM way form the graph's edges. The way's attributes are duplicated across the edges. For example, given the following XML way:
```
  <way id="8636532" version="13" timestamp="2011-01-14T00:47:46Z" changeset="6963395" uid="381909" user="JessAk71">
    <nd ref="61448456"/>
    <nd ref="1102764005"/>
    <nd ref="1099120555"/>
    <nd ref="1099120556"/>
    <nd ref="61420229"/>
    <nd ref="61420222"/>
    <nd ref="61420249"/>
    <nd ref="61420207"/>
    <nd ref="61420214"/>
    <nd ref="643774918"/>
    <tag k="name" v="North Washington Street"/>
    <tag k="width" v="30.2"/>
    <tag k="oneway" v="yes"/>
    <tag k="source" v="massgis_import_v0.1_20071008193615"/>
    <tag k="highway" v="primary"/>
    <tag k="condition" v="fair"/>
    <tag k="attribution" v="Office of Geographic and Environmental Information (MassGIS)"/>
    <tag k="massgis:way_id" v="134349"/>
  </way>
```

```
>>> g[61448456][1102764005]
{'attribution': 'Office of Geographic and Environmental Information (MassGIS)',
 'condition': 'fair',
 'highway': 'primary',
 'massgis:way_id': '134349',
 'name': 'North Washington Street',
 'oneway': 'yes',
 'source': 'massgis_import_v0.1_20071008193615',
 'width': '30.2'}
```

Ways that are not oneway roads will have edges in both directions.

See Also
--------
* [networkx](https://networkx.github.io)
* [OSM QA Tiles](https://osmlab.github.io/osm-qa-tiles/)
* [imposm.parser](https://github.com/omniscale/imposm-paser)
