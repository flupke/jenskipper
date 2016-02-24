import os.path as op

from . import digraph


GRAPH_EDGES_REPRS = {
    'SUCCESS': ' > ',
    'UNSTABLE': ' ?> ',
    'FAILURE': ' ~> ',
}


def get_fname(base_dir):
    '''
    Get the name of the pipelines file in *base_dir*.
    '''
    return op.join(base_dir, 'pipelines.txt')


def format_pipe_bits(bits):
    '''
    Assemble *bits* of a pipeline as text.

    *bits* must be a dict of ``(parents_list, upstream_link_type)`` pairs,
    indexed by job name.
    '''
    graph = digraph.DirectedGraph()
    for child, (parents, upstream_link_type) in bits.items():
        edges_repr = GRAPH_EDGES_REPRS[upstream_link_type]
        for parent in parents:
            graph.add_edge(parent, child, edges_repr)
    return graph.format()
