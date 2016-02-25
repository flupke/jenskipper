import os.path as op

import yaml

from . import pipelines


def get_templates_dir(base_dir):
    return op.join(base_dir, 'templates')


def get_jobs_defs_fname(base_dir):
    return op.join(base_dir, 'jobs.yaml')


def parse_jobs_defs(fp, default_context):
    jobs_defs = yaml.safe_load(fp)
    return {k: _normalize_job_def(v, default_context)
            for k, v in jobs_defs.items()}


def _normalize_job_def(job_def, default_context):
    job_def_context = job_def.get('context', {})
    context = default_context.copy()
    context.update(job_def_context)
    return {
        'template': job_def['template'],
        'context': context,
    }


def get_jobs_defs(base_dir):
    fname = get_jobs_defs_fname(base_dir)
    default_context = get_default_context(base_dir)
    with open(fname) as fp:
        return parse_jobs_defs(fp, default_context)


def get_default_context_fname(base_dir):
    return op.join(base_dir, 'default_context.yaml')


def parse_default_context(fp):
    context = yaml.safe_load(fp)
    if context is None:
        context = {}
    return context


def get_default_context(base_dir):
    fname = get_default_context_fname(base_dir)
    with open(fname) as fp:
        return parse_default_context(fp)


def get_pipelines_fname(base_dir):
    return op.join(base_dir, 'pipelines.txt')


def get_pipelines(base_dir):
    fname = get_pipelines_fname(base_dir)
    with open(fname) as fp:
        return pipelines.parse_pipelines(fp.read())
