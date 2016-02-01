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
    type : string ('xml', 'pbf', or 'qatile')

    >>> graph = parse_data(data, 'xml')

    """
    if type in {'xml', 'pbf'}:
        # If XML or PBF, write to file then call parse
        arg = filename
        return parse_file(filename, **kwargs)
    elif type == 'qatile':
        import osmqa
        importer, parser = _make_importer_parser(osmqa.QATileParser, **kwargs)
        parser.parse_data(data)
        return importer.get_graph()
    else:
        raise ValueError('Unknown data type "%s"' % type)


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
    return parse_data(data, 'qatile', x=x, y=y, zoom=zoom, **kwargs)


def _make_importer_parser(parser_class, **kwargs):
    gi = GraphImporter()
    parser = parser_class(
        coords_callback=gi.coords_callback,
        nodes_callback=gi.nodes_callback,
        ways_callback=gi.ways_callback, 
        **kwargs
    )

    return gi, parser
