osmgraph
========

Create [networkx](https://networkx.github.io/) graphs from OpenStreetMap (OSM)
data.  `osmgraph` uses
[imposm-parser](https://github.com/omniscale/imposm-parser) for parsing raw
OpenStreetMap data. `imposm.parser` provides native readers for XML and PBF
files. You can also use `osmqa-parser` to create graphs from
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
