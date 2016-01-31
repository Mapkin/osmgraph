import itertools

import networkx as nx


class GraphImporter(object):
    def __init__(self):
        self.coords = {}  # node_id -> (lon, lat) tuple
        self.nodes = {}  # node_id -> tags dict
        self.ways = {}  # way_id -> (tags dict, node_id sequence list)

    def add_coords(self, data):
        """ Callback for nodes that have no tags """
        for node_id, lon, lat in data:
            self.coords[node_id] = (lon, lat)

    def add_nodes(self, data):
        """ Callback for nodes with tags """
        for node_id, tags, coords in data:
            # Discard the coords because they go into add_coords
            self.nodes[node_id] = tags

    def add_ways(self, data):
        """ Callback for all ways """
        for way_id, tags, nodes in data:
            # Imposm passes all ways through regardless of whether the tags
            # have been filtered or not. It needs to do this in order to
            # handle relations, but we don't care about relations at the
            # moment.
            if tags:
                self.ways[way_id] = (tags, nodes)

    def get_graph(self):
        """ Return the networkx directed graph of received data """
        g = nx.DiGraph()

        for way_id, (tags, nodes) in self.ways.items():
            oneway = tags.get('oneway')
            # If oneway is '-1', reverse the way and treat as a normal oneway
            if oneway == '-1':
                nodes = reversed(nodes)
                oneway = 'yes'
            backward = oneway != 'yes'

            for n0, n1 in pairwise(nodes):
                g.add_edge(n0, n1, **tags)
                if backward:
                    g.add_edge(n1, n0, **tags)

                g.node[n0].update(self._node_properties(n0))
            g.node[n1].update(self._node_properties(n1))

        return g

    def _node_properties(self, node_id):
        properties = self.nodes.get(node_id, {})
        properties['coordinate'] = self.coords[node_id]
        return properties


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    # From itertools docs: https://docs.python.org/2/library/itertools.html
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)
