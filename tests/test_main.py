import osmgraph.main


class FakeParser(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def test_default_ways_tag_filter():
    importer, parser = osmgraph.main.make_importer_parser(FakeParser)

    assert (parser.kwargs['ways_tag_filter'] is
            osmgraph.main.default_ways_tag_filter)


def test_none_ways_tag_filter():
    importer, parser = osmgraph.main.make_importer_parser(
        FakeParser, ways_tag_filter=None
    )

    assert parser.kwargs['ways_tag_filter'] is None


def test_custom_ways_tag_filter():
    def custom_filter(tags):
        pass

    importer, parser = osmgraph.main.make_importer_parser(
        FakeParser, ways_tag_filter=custom_filter
    )

    assert parser.kwargs['ways_tag_filter'] is custom_filter
