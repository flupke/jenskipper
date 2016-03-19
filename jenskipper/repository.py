import os
import os.path as op
import sys

import yaml
import click

from . import pipelines
from . import jobs


CONF_FNAME = '.jenskipper.conf'


def search_base_dir(from_dir='.', up_to_dir='/'):
    '''
    Search the base dir of a jenskipper repository.

    The search starts at *from_dir* and continues in parent directories, up to
    *up_to_dir* or when a directory that looks like a jenskipper repository is
    found.

    Return the base directory of the repository, or None.
    '''
    cur_dir = op.abspath(from_dir)
    while cur_dir != up_to_dir:
        if CONF_FNAME in os.listdir(cur_dir):
            return cur_dir
        cur_dir = op.dirname(cur_dir)


def check_dir_is_in_repository(from_dir, retcode=1):
    '''
    Check if *from_dir* does belong to a jenskipper repository.

    If it doesn't, print an error message and exit program with *retcode*. If
    it does, return the base directory of the repository.
    '''
    base_dir = search_base_dir(from_dir)
    if base_dir is None:
        click.secho('Could not find a jenskipper repository in "%s" and its '
                    'parent directories' % from_dir, fg='red', bold=True)
        sys.exit(1)
    return base_dir


def get_templates_dir(base_dir):
    return op.join(base_dir, 'templates')


def get_jobs_defs_fname(base_dir):
    return op.join(base_dir, 'jobs.yaml')


def parse_jobs_defs(fp, default_contexts):
    jobs_defs = yaml.safe_load(fp)
    return {k: _normalize_job_def(v, default_contexts)
            for k, v in jobs_defs.items()}


def _normalize_job_def(job_def, default_contexts):
    job_def_context = job_def.get('context', {})
    default_context_name = job_def.get('default_context', 'default')
    context = default_contexts.get(default_context_name, {}).copy()
    context.update(job_def_context)
    return {
        'template': job_def['template'],
        'default_context': default_context_name,
        'context': context,
    }


def get_jobs_defs(base_dir):
    '''
    Get the jobs definitons for the repository in *base_dir*.

    Return a dict indexed by job name containing jobs properties (template,
    context, etc...).
    '''
    fname = get_jobs_defs_fname(base_dir)
    default_contexts = get_default_contexts(base_dir)
    with open(fname) as fp:
        return parse_jobs_defs(fp, default_contexts)


def get_default_contexts_fname(base_dir):
    return op.join(base_dir, 'contexts.yaml')


def parse_default_contexts(fp):
    contexts = yaml.safe_load(fp)
    if contexts is None:
        contexts = {}
    return contexts


def get_default_contexts(base_dir):
    fname = get_default_contexts_fname(base_dir)
    with open(fname) as fp:
        return parse_default_contexts(fp)


def get_pipelines_fname(base_dir):
    return op.join(base_dir, 'pipelines.txt')


def get_pipelines(base_dir):
    fname = get_pipelines_fname(base_dir)
    with open(fname) as fp:
        return pipelines.parse_pipelines(fp.read())


def get_conf_fname(base_dir):
    return op.join(base_dir, CONF_FNAME)


def get_job_conf(base_dir, job_name, context_overrides={}):
    jobs_defs = get_jobs_defs(base_dir)
    pipelines = get_pipelines(base_dir)
    job_def = jobs_defs[job_name]
    pipe_info = pipelines.get(job_name)
    templates_dir = get_templates_dir(base_dir)
    return jobs.render_job(templates_dir, job_def['template'],
                           job_def['context'], pipe_info,
                           context_overrides=context_overrides)
