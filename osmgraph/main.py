import os
import tempfile
import urllib

from imposm.parser import OSMParser

from .importer import GraphImporter


def parse_file(filename, **kwargs):
    """
    Return an OSM networkx graph from the input OSM file

    Only works with OSM xml, xml.bz2 and pbf files. This function cannot take
    OSM QA tile files. Use parse_qa_tile() for QA tiles.

    >>> graph = parse_file(filename)

    """
    importer, parser = make_importer_parser(OSMParser, **kwargs)
    parser.parse(filename)

    return importer.get_graph()


def parse_data(data, type, **kwargs):
    """
    Return an OSM networkx graph from the input OSM data

    Parameters
    ----------
    data : string
    type : string ('xml' or 'pbf')

    >>> graph = parse_data(data, 'xml')

    """
    suffixes = {
        'xml': '.osm',
        'pbf': '.pbf',
    }
    try:
        suffix = suffixes[type]
    except KeyError:
        raise ValueError('Unknown data type "%s"' % type)

    fd, filename = tempfile.mkstemp(suffix=suffix)
    try:
        os.write(fd, data)
        os.close(fd)
        return parse_file(filename, **kwargs)
    finally:
        os.remove(filename)


def parse_qa_tile(x, y, zoom, data, **kwargs):
    """
    Return an OSM networkx graph from the input OSM QA tile data

    Parameters
    ----------
    data : string
    x : int
        tile's x coordinate
    y : int
        tile's y coordinate
    zoom : int
        tile's zoom level

    >>> graph = parse_qa_tile(data, 1239, 1514, 12)

    """
    import osmqa
    importer, parser = make_importer_parser(osmqa.QATileParser, **kwargs)
    parser.parse_data(x, y, zoom, data)
    return importer.get_graph()


def parse_bbox(bbox, **kwargs):
    """
    Download OSM data from a bounding box and parse into a graph

    Parameters
    ----------
    bbox : (west, south, east, north) tuple of 4 floats

    >>> graph = parse_bbox([-71.06643, 42.36051, -71.06253, 42.36358])

    """
    data = _dowload_osm_bbox(bbox)
    return parse_data(data, 'xml', **kwargs)


def make_importer_parser(parser_class, **kwargs):
    gi = GraphImporter()

    if 'ways_tag_filter' not in kwargs:
        kwargs['ways_tag_filter'] = default_ways_tag_filter

    parser = parser_class(
        coords_callback=gi.coords_callback,
        nodes_callback=gi.nodes_callback,
        ways_callback=gi.ways_callback,
        **kwargs
    )

    return gi, parser


def default_ways_tag_filter(tags):
    if 'highway' not in tags:
        tags.clear()


def _dowload_osm_bbox(bbox):
    bbox_arg = urllib.urlencode({'bbox': ','.join(str(x) for x in bbox)})
    url = 'http://openstreetmap.org/api/0.6/map?' + bbox_arg
    response = urllib.urlopen(url)
    if response.code != 200:
        raise ValueError('Received %s from OSM' % response.code)
    content = response.read()
    response.close()

    return content
