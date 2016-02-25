import os.path as op
from xml.etree import ElementTree

import jinja2
import yaml


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
    pruned_conf = ElementTree.tostring(tree, encoding='UTF-8', method='xml')
    return pipe_bits, pruned_conf


def merge_pipeline_conf(conf):
    pass


def create_templates_env(base_dir='.'):
    templates_dir = get_templates_dir(base_dir)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))


def get_templates_dir(base_dir):
    return op.join(base_dir, 'templates')


def get_default_template_fname(base_dir, job_name):
    templates_dir = get_templates_dir(base_dir)
    return op.join(templates_dir, job_name, 'config.xml')


def get_jobs_defs_fname(base_dir):
    return op.join(base_dir, 'jobs.yaml')


def get_default_context_fname(base_dir):
    return op.join(base_dir, 'default_context.yaml')


def format_default_jobs_defs(jobs_templates, base_dir):
    '''
    Format the default jobs definitions on initial import.
    '''
    lines = []
    templates_dir = get_templates_dir(base_dir)
    for job_name in sorted(jobs_templates):
        template_fname = jobs_templates[job_name]
        rel_template_fname = template_fname[len(templates_dir) + 1:]
        lines.append('%s:' % job_name)
        lines.append('  template: %s' % rel_template_fname)
        lines.append('')
    return '\n'.join(lines)


def parse_jobs(fp, base_dir, default_context):
    jobs_defs = yaml.safe_load(fp)
    return {k: _normalize_job_def(v, base_dir, default_context)
            for k, v in jobs_defs.items()}


def _normalize_job_def(job_def, base_dir, default_context):
    job_def_context = job_def.get('context', {})
    context = default_context.copy()
    context.update(job_def_context)
    return {
        'template': job_def['template'],
        'context': context,
    }


def render_jobs(jobs_defs, pipelines, base_dir):
    ret = {}
    env = create_templates_env(base_dir)
    for job_name, job_def in jobs_defs.items():
        template = env.get_template(job_def['template'])
        rendered = template.render(**job_def['context'])
        merged = merge_pipeline_conf(rendered, pipelines)
        ret[job_name] = merged
    return merged
