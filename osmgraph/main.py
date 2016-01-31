from imposm.parser import OSMParser

from .importer import GraphImporter


def parse_file(filename, **kwargs):
    importer, parser = _make_importer_parser(OSMParser, **kwargs)
    parser.parse(filename)

    return importer.get_graph()


def parse_data(data, type, **kwargs):
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
    return parse_data(data, 'qatile', x=x, y=y, zoom=zoom, **kwargs)


def _make_importer_parser(parser_class, **kwargs):
    gi = GraphImporter()
    parser = parser_class(
        coords_callback=gi.add_coords,
        nodes_callback=gi.add_nodes,
        ways_callback=gi.add_ways, 
        **kwargs
    )

    return gi, parser
