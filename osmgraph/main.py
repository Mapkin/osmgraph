from imposm.parser import OSMParser

from .importer import GraphImporter


def parse_file(filename, **kwargs):
    """
    Return an OSM networkx graph from the input OSM file

    Only works with OSM xml, xml.bz2 and pbf files. This function cannot take
    OSM QA tile files. Use parse_qa_tile() for QA tiles.

    >>> graph = parse_file(filename)

    """
    importer, parser = _make_importer_parser(OSMParser, **kwargs)
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
    if type not in {'xml', 'pbf'}:
        raise ValueError('Unknown data type "%s"' % type)
    # TODO: Write out a temporary file and call parse_file
    raise NotImplementedError()


def parse_qa_tile(data, x, y, zoom, **kwargs):
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
    importer, parser = _make_importer_parser(osmqa.QATileParser, **kwargs)
    parser.parse_data(data, x, y, zoom)
    return importer.get_graph()


def _make_importer_parser(parser_class, **kwargs):
    gi = GraphImporter()
    parser = parser_class(
        coords_callback=gi.coords_callback,
        nodes_callback=gi.nodes_callback,
        ways_callback=gi.ways_callback, 
        **kwargs
    )

    return gi, parser
