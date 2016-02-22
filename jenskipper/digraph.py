import copy
from collections import defaultdict

from .exceptions import CyclicDependency


def split_connected_graphs(graph):
    '''
    Separate unconnected graphs in *graph* from each other.

    Return a list of :class:`DirectedGraph` objects that are garanteed to
    contain only connected components.
    '''
    graph = graph.copy()
    ret = []
    while graph.nodes:
        node = graph.nodes.values()[0]
        subgraph = DirectedGraph()
        for parent, child in list(graph.walk_edges_from(node)):
            subgraph.add_edge(parent, child)
            graph.remove_node(parent)
            graph.remove_node(child)
        ret.append(subgraph)
    return ret


def topo_sort(graph):
    '''
    Make a topological sort on *graph*.

    Return sorted node names.

    Raise :class:`~bundle.exceptions.CyclicDependency` if one or more cyclic
    dependencies are found.
    '''
    graph = graph.copy()

    stack = graph.roots()
    sorted_nodes = []
    while stack:
        node = stack.pop()
        sorted_nodes.append(node)
        for child in graph.children[node].copy():
            graph.remove_edge(node, child)
            if not graph.parents[child]:
                stack.append(child)
    graph.gc()
    if graph.nodes:
        raise CyclicDependency(graph.nodes.values())

    return [n.name for n in sorted_nodes]


class DirectedGraph(object):

    def __init__(self):
        self.nodes = {}
        self.children = defaultdict(set)
        self.parents = defaultdict(set)

    def iter_edges(self):
        for parent, children in self.children.items():
            for child in children:
                yield (parent, child)

    def add_node(self, name):
        if name not in self.nodes:
            node = Node(name)
            self.nodes[name] = node
        node = self.nodes[name]
        return node

    def remove_node(self, name):
        if name in self.nodes:
            del self.nodes[name]
            self.children[name].clear()
            self.parents[name].clear()
            for children in self.children.values():
                children.discard(name)
            for parents in self.parents.values():
                parents.discard(name)

    def add_edge(self, parent, child):
        parent_node = self.add_node(parent)
        child_node = self.add_node(child)
        self.children[parent].add(child_node)
        self.parents[child].add(parent_node)

    def add_edges_list(self, *edges):
        for parent, child in edges:
            self.add_edge(parent, child)

    def remove_edge(self, parent, child):
        self.children[parent].discard(child)
        self.parents[child].discard(parent)

    def copy(self):
        return copy.deepcopy(self)

    def roots(self):
        '''
        Return the list of nodes that have no parents.
        '''
        return [n for n in self.nodes.values() if not self.parents[n]]

    def gc(self):
        '''
        Delete all detached nodes.
        '''
        for name in self.nodes.keys():
            if not self.children[name] and not self.parents[name]:
                del self.nodes[name]

    def walk_edges_from(self, node):
        '''
        An iterator traversing the whole graph, starting from *node*.

        Yields ``(parent, child)`` node pairs.
        '''
        stack = [node]
        visited = set()
        while stack:
            cur_node = stack.pop()
            visited.add(cur_node)
            for child in self.children[cur_node].copy():
                yield (cur_node, child)
            for container in (self.children[cur_node], self.parents[cur_node]):
                for conn_node in container:
                    if conn_node not in visited:
                        visited.add(conn_node)
                        stack.append(conn_node)


class Node(object):
    '''
    A node of a :class:`DirectedGraph`.

    It has the property of being interchangeable with its *name* when used as
    dict keys.
    '''

    def __init__(self, name):
        if isinstance(name, Node):
            name = name.name
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        return self.name == other

    def __repr__(self):
        return '<Node %r>' % self.name

    def __str__(self):
        return str(self.name)
