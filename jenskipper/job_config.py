from xml.etree import ElementTree


def extract_pipeline_conf(conf):
    '''
    Remove and parse the pipeline bits in XML job definition *conf*.
    '''
    tree = ElementTree.fromstring(conf)
    parent_map = {c: p for p in tree.iter() for c in p}
    rbt_elt = tree.find('.//jenkins.triggers.ReverseBuildTrigger')
    if rbt_elt is not None:
        upstream_projects = rbt_elt.findtext('./upstreamProjects')
        upstream_projects = [x for x in upstream_projects.split(',')
                             if x.strip()]
        upstream_link_type = rbt_elt.findtext('./threshold/name')
        pipe_bits = (upstream_projects, upstream_link_type)
    else:
        pipe_bits = None
    parent_map[rbt_elt].remove(rbt_elt)
    pruned_conf = ElementTree.tostring(tree)
    return pipe_bits, pruned_conf


def merge_pipeline_conf(conf):
    pass
