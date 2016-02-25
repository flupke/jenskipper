from xml.etree import ElementTree

import jinja2

from . import repository


LINK_ELTS = {
    'SUCCESS': (
        ('ordinal', '0'),
        ('color', 'BLUE'),
        ('completeBuild', 'true'),
    ),
    'UNSTABLE': (
        ('ordinal', '1'),
        ('color', 'YELLOW'),
        ('completeBuild', 'true'),
    ),
    'FAILURE':  (
        ('ordinal', '2'),
        ('color', 'RED'),
        ('completeBuild', 'true'),
    ),
}


def extract_pipeline_conf(conf):
    '''
    Remove and parse the pipeline bits in XML job definition *conf*.
    '''
    tree = ElementTree.fromstring(conf.encode('utf8'))
    rbt_elt = tree.find('.//jenkins.triggers.ReverseBuildTrigger')
    if rbt_elt is not None:
        upstream_projects = rbt_elt.findtext('./upstreamProjects')
        upstream_projects = [x for x in upstream_projects.split(',')
                             if x.strip()]
        upstream_link_type = rbt_elt.findtext('./threshold/name')
        pipe_bits = (upstream_projects, upstream_link_type)
        parent_map = {c: p for p in tree.iter() for c in p}
        parent_map[rbt_elt].remove(rbt_elt)
    else:
        pipe_bits = None
    pruned_conf = _format_xml_tree(tree)
    return pipe_bits, pruned_conf


def _format_xml_tree(tree):
    return ElementTree.tostring(tree, encoding='UTF-8', method='xml')


def merge_pipeline_conf(conf, parents, link_type):
    '''
    Merge back pipeline informations in job configuration *conf*.

    *parents* is a list of parent jobs names, and *link_type* the relationship
    to them (one of "SUCCESS", "UNSTABLE" or "FAILURE").
    '''
    tree = ElementTree.fromstring(conf.encode('utf8'))
    trigger = _create_elt('jenkins.triggers.ReverseBuildTrigger')
    trigger.append(_create_elt('spec'))
    upstream_projects = _create_elt('upstreamProjects', ', '.join(parents))
    trigger.append(upstream_projects)
    threshold = _create_elt('threshold')
    threshold.append(_create_elt('name', link_type))
    for elt_name, elt_text in LINK_ELTS[link_type]:
        elt = _create_elt(elt_name, elt_text)
        threshold.append(elt)
    trigger.append(threshold)
    triggers = tree.find('.//triggers')
    triggers.append(trigger)
    return _format_xml_tree(tree)


def _create_elt(tag, text=None):
    elt = ElementTree.Element(tag)
    elt.text = text
    return elt


def render_job(job_def, pipe_info, base_dir):
    templates_dir = repository.get_templates_dir(base_dir)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
    template = env.get_template(job_def['template'])
    rendered = template.render(**job_def['context'])
    if pipe_info is not None:
        parents, link_type = pipe_info
        rendered = merge_pipeline_conf(rendered, parents, link_type)
    return rendered
