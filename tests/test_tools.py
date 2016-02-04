from __future__ import absolute_import

import networkx as nx
import pytest

from osmgraph import tools


def test_coordinates():
    g = nx.DiGraph()

    c1, c2, c3 = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]
    g.add_node(1, attr_dict={'coordinate': c1})
    g.add_node(2, attr_dict={'coordinate': c2})
    g.add_node(3, attr_dict={'coordinate': c3})
    g.add_edges_from([(1, 2), (2, 3)])

    assert tools.coordinates(g, (1, 2, 3)) == [c1, c2, c3]


def test_nwise_3():
    x = list(range(10))

    expected = [
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 4),
        (3, 4, 5),
        (4, 5, 6),
        (5, 6, 7),
        (6, 7, 8),
        (7, 8, 9),
    ]
    assert list(tools.nwise(x, 3)) == expected


def test_nwise_4():
    x = list(range(10))

    expected = [
        (0, 1, 2, 3),
        (1, 2, 3, 4),
        (2, 3, 4, 5),
        (3, 4, 5, 6),
        (4, 5, 6, 7),
        (5, 6, 7, 8),
        (6, 7, 8, 9),
    ]
    assert list(tools.nwise(x, 4)) == expected


def test_pairwise():
    x = list(range(10))

    expected = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
    ]
    assert list(tools.pairwise(x)) == expected


@pytest.fixture
def tgraph():
    #
    #
    #  1 -- 2 -- 3 -->-- 5 -->-- 7
    #            |       |
    #            ^       v
    #            |       |
    #            4       6
    #
    g = nx.DiGraph()
    g.add_edges_from([
        (1, 2),
        (2, 1),
        (2, 3),
        (3, 2),
        (4, 3),
        (3, 5),
        (5, 6),
        (5, 7),
    ])

    return g


def test_step_basic(tgraph):
    assert tools.step(tgraph, 1, 2) == 3


def test_step_inbound_false(tgraph):
    assert tools.step(tgraph, 2, 3) == 5


def test_step_inbound_true(tgraph):
    assert tools.step(tgraph, 2, 3, inbound=True) is None


def test_step_stop(tgraph):
    assert tools.step(tgraph, 3, 5) is None


def test_move(tgraph):
    assert list(tools.move(tgraph, 1, 2)) == [1, 2, 3, 5]


def test_move_inbound(tgraph):
    assert list(tools.move(tgraph, 1, 2, inbound=True)) == [1, 2, 3]
