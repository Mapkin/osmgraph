import itertools

import geog


def nwise(iterable, n):
    """
    Iterate through a sequence with a defined length window

    >>> list(nwise(range(8), 3))
    [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (5, 6, 7)]

    >>> list(nwise(range(3), 5))
    []


    Parameters
    ----------
    iterable
    n : length of each sequence

    Yields
    ------
    Tuples of length n

    """
    iters = itertools.tee(iterable, n)
    iters = (itertools.islice(it, i, None) for i, it in enumerate(iters))
    return itertools.izip(*iters)


def pairwise(iterable):
    """
    Iterate over pairs of input iterable.

    Shortcut for nwise(iterable, 2)

    >>> list(pairwise(range(5)))
    [(0, 1), (1, 2), (2, 3), (3, 4)]

    """
    return nwise(iterable, 2)


def coordinates(g, nodes):
    """
    Extract (lon, lat) coordinate pairs from nodes in an osmgraph

    osmgraph nodes have a 'coordinate' property on each node. This is
    a shortcut for extracting a coordinate list from an iterable of nodes

    >>> g = osmgraph.parse_file(filename)
    >>> node_ids = g.nodes()[:3]  # Grab 3 nodes
    [61341696, 61341697, 61341698]
    >>> coords = coordinates(g, node_ids)
    [(-71.0684107, 42.3516822),
     (-71.133251, 42.350308),
     (-71.170641, 42.352689)]


    Parameters
    ----------
    g : networkx graph created with osmgraph
    nodes : iterable of node ids

    Returns
    -------
    List of (lon, lat) coordinate pairs

    """
    c = [g.node[n]['coordinate'] for n in nodes]
    return c


def step(g, n1, n2, inbound=False, backward=False, continue_fn=None):
    """
    Step along a path through a directed graph unless there is an intersection

    Example graph:
    Note that edge (1, 2) and (2, 3) are bidirectional, i.e., (2, 1) and
    (3, 2) are also edges

    1 -- 2 -- 3 -->-- 5 -->-- 7
              |       |
              ^       v
              |       |
              4       6

    >>> step(g, 1, 2)
    3
    >>> step(g, 3, 5)
    None

    >>> step(g, 2, 3)
    5
    >>> step(g, 2, 3, inbound=True)
    None

    >>> step(g, 7, 5, 3, backward=True)
    3

    >>> def f(g, n1, n2, backward):
            if n2 == 5:
                return 7
            return None
    >>> step(g, 3, 5, continue_fn=f)
    7


    Parameters
    ----------
    g : networkx DiGraph
    n1 : node id in g
    n2 : node id in g
        (n1, n2) must be an edge in g
    inbound : bool (default False)
        whether incoming edges should be considered
    backward : bool (default False)
        whether edges are in reverse order (i.e., point from n2 to n1)
    continue_fn : callable (optional)
        if at an intersection, continue_fn is called to indicate how to
        proceed

        continue_fn takes the form:
        f(g, n1, n2, backward) where all arguments are as passed into step.
        f should return a node id such that f(g, n1, n2, backward) is a
        successors of n2. f should return None if no way forward.

    Returns
    -------
    The next node in the path from n1 to n2. Returns None if there
    are no edges from n2 or multiple edges from n2

    """
    forw = g.successors
    back = g.predecessors
    if backward:
        back, forw = forw, back

    nodes = forw(n2)
    if inbound:
        nodes = set(nodes + back(n2))
    candidates = [n for n in nodes if n != n1]

    if len(candidates) == 1:
        result = candidates[0]
    elif continue_fn:
        result = continue_fn(g, n1, n2, backward)
    else:
        result = None
    return result


def move(g, n1, n2, **kwargs):
    """
    Step along a graph until it ends or reach an intersection

    Example graph:
    Note that edge (1, 2) and (2, 3) are bidirectional, i.e., (2, 1) and
    (3, 2) are also edges

    1 -- 2 -- 3 -->-- 5 -->-- 7
              |       |
              ^       v
              |       |
              4       6

    >>> list(move(g, 1, 2))
    [1, 2, 3, 5]  # Stops at 5 because you can get to both 6 and 7 from 3

    >>> step(g, 1, 2, inbound=True)
    [1, 2, 3]


    Parameters
    ----------
    Same as step()

    Yields
    ------
    Node IDs until either there is no path forward or the path reaches
    an intersection

    """
    prev = n1
    curr = n2
    _next = step(g, prev, curr, **kwargs)

    yield prev
    yield curr

    visited_nodes = set([prev, curr])
    while _next:
        yield _next
        if _next in visited_nodes:
            return
        visited_nodes.add(_next)
        prev = curr
        curr = _next
        _next = step(g, prev, curr, **kwargs)


def is_intersection(g, n):
    """
    Determine if a node is an intersection

    graph: 1 -->-- 2 -->-- 3

    >>> is_intersection(g, 2)
    False

    graph:
     1 -- 2 -- 3
          |
          4

    >>> is_intersection(g, 2)
    True

    Parameters
    ----------
    g : networkx DiGraph
    n : node id

    Returns
    -------
    bool

    """
    return len(set(g.predecessors(n) + g.successors(n))) > 2


def turn_angle(g, n1, n2, n3):
    coords = coordinates(g, [n1, n2, n3])
    return turn_angle_coords(coords)


def turn_angle_coords(coords):
    if len(coords) != 3:
        raise ValueError('coords must have length 3')

    angles = geog.course(coords[:-1], coords[1:])

    a = angles[1] - angles[0]
    if a < -180:
        a += 360
    elif a > 180:
        a -= 360

    return a
