import os.path as op
from xml.etree import ElementTree


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
    pruned_conf = ElementTree.tostring(tree)
    return pipe_bits, pruned_conf


def merge_pipeline_conf(conf):
    pass


def get_default_template_fname(base_dir, job_name):
    return op.join(base_dir, 'templates', job_name, 'config.xml')


def get_jobs_defs_fname(base_dir):
    return op.join(base_dir, 'jobs.yaml')


def get_default_context_fname(base_dir):
    return op.join(base_dir, 'default_context.yaml')


def format_default_jobs_defs(jobs_templates, dest_dir):
    lines = []
    for job_name in sorted(jobs_templates):
        template_fname = jobs_templates[job_name]
        rel_template_fname = template_fname[len(dest_dir) + 1:]
        lines.append('%s:' % job_name)
        lines.append('  template: %s' % rel_template_fname)
        lines.append('')
    return '\n'.join(lines)
