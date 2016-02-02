osmgraph
========

Create [networkx](https://networkx.github.io/) graphs from OpenStreetMap (OSM)
data.  `osmgraph` uses
[imposm-parser](https://github.com/omniscale/imposm-parser) for parsing
OpenStreetMap XML and PBF
files and [osmqa-parser](https://github.com/mapkin/osmqa-parser) for parsing
[OSM QA tiles](http://osmlab.github.io/osm-qa-tiles/).


Usage
-----

```
>>> import osmgraph
>>> g = osmgraph.parse_file(filename)

```


Graph Structure
--------------
TODO

See Also
--------
* [networkx](https://networkx.github.io)
* [OSM QA Tiles](https://osmlab.github.io/osm-qa-tiles/)
* [imposm.parser](https://github.com/omniscale/imposm-paser)
