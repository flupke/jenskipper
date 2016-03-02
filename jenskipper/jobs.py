from xml.etree import ElementTree
import hashlib

import jinja2


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
    tree = ElementTree.fromstring(conf)
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
    tree = ElementTree.fromstring(conf)
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


def render_job(job_def, pipe_info, templates_dir):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir),
                             autoescape=True,
                             undefined=jinja2.StrictUndefined)
    template = env.get_template(job_def['template'])
    rendered = template.render(**job_def['context'])
    rendered = rendered.encode('utf8')
    if pipe_info is not None:
        parents, link_type = pipe_info
        rendered = merge_pipeline_conf(rendered, parents, link_type)
    return rendered


def get_conf_hash(conf):
    '''
    Get a hash uniquely representing the XML job configuration *conf*.
    '''
    hobj = hashlib.sha1()
    tree = ElementTree.fromstring(conf)
    for element in tree.iter():
        hobj.update(element.tag)
        if element.text is not None:
            hobj.update(element.text)
        for key in sorted(element.attrib):
            value = element.attrib[key]
            hobj.update(key)
            hobj.update(value)
    return hobj.hexdigest()


def append_hash_in_comments(conf):
    '''
    Append the *conf* hash at the end of its description.
    '''
    conf_hash = get_conf_hash(conf)
    tree = ElementTree.fromstring(conf)
    description_elt = tree.find('.//description')
    text = description_elt.text if description_elt.text is not None else ''
    text += '\r\n\r\n-*- jenskipper-hash: %s -*-' % conf_hash
    description_elt.text = text
    return _format_xml_tree(tree)
