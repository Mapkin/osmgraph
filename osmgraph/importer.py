import itertools

import networkx as nx

from . import tools


class GraphImporter(object):
    def __init__(self):
        self.coords = {}  # node_id -> (lon, lat) tuple
        self.nodes = {}  # node_id -> tags dict
        self.ways = {}  # way_id -> (tags dict, node_id sequence list)

    def coords_callback(self, data):
        """ Callback for nodes that have no tags """
        for node_id, lon, lat in data:
            self.coords[node_id] = (lon, lat)

    def nodes_callback(self, data):
        """ Callback for nodes with tags """
        for node_id, tags, coords in data:
            # Discard the coords because they go into add_coords
            self.nodes[node_id] = tags

    def ways_callback(self, data):
        """ Callback for all ways """
        for way_id, tags, nodes in data:
            # Imposm passes all ways through regardless of whether the tags
            # have been filtered or not. It needs to do this in order to
            # handle relations, but we don't care about relations at the
            # moment.
            if tags:
                self.ways[way_id] = (tags, nodes)

    def get_graph(self, parse_direction=False):
        """ Return the networkx directed graph of received data """
        g = nx.DiGraph()

        for way_id, (tags, nodes) in self.ways.items():
            # If oneway is '-1', reverse the way and treat as a normal oneway
            if tags.get('oneway') == '-1':
                nodes = reversed(nodes)
                tags['oneway'] = 'yes'
            oneway = tags.get('oneway') == 'yes'

            for n0, n1 in tools.pairwise(nodes):
                g.add_edge(n0, n1, attr_dict=tags)
                if parse_direction:
                    g[n0][n1]['_direction'] = 'forward'
                if not oneway:
                    g.add_edge(n1, n0, attr_dict=tags)
                    if parse_direction:
                        g[n1][n0]['_direction'] = 'backward'

                g.node[n0].update(self._node_properties(n0))
            g.node[n1].update(self._node_properties(n1))

        return g

    def _node_properties(self, node_id):
        properties = self.nodes.get(node_id, {})
        properties['coordinate'] = self.coords[node_id]
        return properties
