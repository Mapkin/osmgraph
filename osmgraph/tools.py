import itertools

import geog


def nwise(iterable, n):
    iters = itertools.tee(iterable, n)
    iters = (itertools.islice(it, i, None) for i, it in enumerate(iters))
    return itertools.izip(*iters)


def pairwise(iterable):
    return nwise(iterable, 2)


def coordinates(g, nodes):
    c = [g.node[n]['coordinate'] for n in nodes]
    return c


def step(g, n1, n2, inbound=False):
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


    Parameters
    ----------
    g : networkx DiGraph
    n1 : node id in g
    n2 : node id in g
        (n1, n2) must be an edge in g
    inbound : bool (default False)
        whether incoming edges should be considered

    Returns
    -------
    The next node in the path from n1 to n2. Returns None if there
    are no edges from n2 or multiple edges from n2

    """
    nodes = g.successors(n2)
    if inbound:
        nodes = set(nodes + g.predecessors(n2))
    candidates = [n for n in nodes if n != n1]

    if len(candidates) == 1:
        return candidates[0]
    return None


def move(g, n1, n2, inbound=False):
    prev = n1
    curr = n2
    _next = step(g, prev, curr, inbound=inbound)

    yield prev
    yield curr
    while _next:
        yield _next
        prev = curr
        curr = _next
        _next = step(g, prev, curr, inbound=inbound)


def turn_angle(g, n1, n2, n3):
    coords = coordinates(g, [n1, n2, n3])
    angles = geog.course(coords[:-1], coords[1:])

    a = angles[1] - angles[0]
    if a < -180:
        a += 360
    elif a > 180:
        a -= 360

    return a
