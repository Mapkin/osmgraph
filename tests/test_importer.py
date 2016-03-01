from osmgraph.importer import GraphImporter


def test_importer():
    gi = GraphImporter()

    coords = [
        (0, 1.0, 2.0),
        (1, 3.0, 4.0),
        (2, 5.0, 6.0),
        (3, 7.0, 8.0),
        (4, 9.0, 10.0),
        (5, 11.0, 12.0),
        (6, 13.0, 14.0),
        (7, 15.0, 16.0),
        (8, 17.0, 18.0),
        (9, 19.0, 20.0),
    ]
    gi.coords_callback(coords)
    nodes = [
        (1, {'key1': 'value1'}, (None, None)),
        (3, {'key2': 'value2'}, (None, None)),
    ]
    gi.nodes_callback(nodes)

    ways = [
        (1, {'key3': 'value3'}, [0, 1, 2]),
        (2, {}, [8, 9]),  # no tags, should be absent from graph
        (3, {'key4': 'value4', 'oneway': 'yes'}, [2, 3, 4, 5]),
        (4, {'oneway': '-1'}, [7, 6, 5]),
    ]
    gi.ways_callback(ways)

    g = gi.get_graph()

    expected_nodes = [
        (0, {'coordinate': (1.0, 2.0)}),
        (1, {'coordinate': (3.0, 4.0), 'key1': 'value1'}),
        (2, {'coordinate': (5.0, 6.0)}),
        (3, {'coordinate': (7.0, 8.0), 'key2': 'value2'}),
        (4, {'coordinate': (9.0, 10.0)}),
        (5, {'coordinate': (11.0, 12.0)}),
        (6, {'coordinate': (13.0, 14.0)}),
        (7, {'coordinate': (15.0, 16.0)}),
    ]
    expected_edges = [
        (0, 1, {'key3': 'value3'}),
        (1, 0, {'key3': 'value3'}),
        (1, 2, {'key3': 'value3'}),
        (2, 1, {'key3': 'value3'}),
        (2, 3, {'key4': 'value4', 'oneway': 'yes'}),
        (3, 4, {'key4': 'value4', 'oneway': 'yes'}),
        (4, 5, {'key4': 'value4', 'oneway': 'yes'}),
        (5, 6, {'oneway': 'yes'}),
        (6, 7, {'oneway': 'yes'}),
    ]
    assert sorted(g.nodes(data=True)) == expected_nodes
    assert sorted(g.edges(data=True)) == expected_edges


def test_u_v_edges():
    gi = GraphImporter()

    coords = [
        (0, 1.0, 2.0),
        (1, 3.0, 4.0),
    ]
    gi.coords_callback(coords)

    ways = [
        (1, {'u': 'value1', 'v': 'value2'}, [0, 1]),
    ]
    gi.ways_callback(ways)

    g = gi.get_graph()

    expected_edges = [
        (0, 1, {'u': 'value1', 'v': 'value2'}),
        (1, 0, {'u': 'value1', 'v': 'value2'})
    ]
    assert sorted(g.edges(data=True)) == expected_edges


def test_parse_direction():
    gi = GraphImporter()

    coords = [
        (0, 1.0, 2.0),
        (1, 3.0, 4.0),
    ]
    gi.coords_callback(coords)

    ways = [
        (1, {'u': 'value1', 'v': 'value2'}, [0, 1]),
    ]
    gi.ways_callback(ways)

    g = gi.get_graph(parse_direction=True)

    assert g[0][1]['_direction'] == 'forward'
    assert g[1][0]['_direction'] == 'backward'
