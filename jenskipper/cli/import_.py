import os
import os.path as op
import sys

import click

from .. import jenkins_api
from .. import jobs
from .. import pipelines


@click.command('import')
@click.argument('jenkins_url')
@click.argument('dest_dir')
def import_(jenkins_url, dest_dir):
    '''
    Import jobs from JENKINS_URL into DEST_DIR.
    '''
    if op.exists(dest_dir):
        click.secho('Destination dir "%s" already exists' % dest_dir, fg='red')
        sys.exit(1)
    jobs_names = jenkins_api.list_jobs(jenkins_url)
    with click.progressbar(jobs_names, label='Importing jobs') as bar:
        pipes_bits, jobs_templates = _write_jobs_templates(bar, dest_dir,
                                                           jenkins_url)
    _write_jobs_defs(jobs_templates, dest_dir)
    _write_pipelines(pipes_bits, dest_dir)
    _write_default_context(dest_dir)


def _write_jobs_templates(jobs_names, dest_dir, jenkins_url):
    pipes_bits = {}
    jobs_templates = {}
    for job_name in jobs_names:
        config = jenkins_api.get_job_config(jenkins_url, job_name)
        pipe_info, conf = jobs.extract_pipeline_conf(config)
        if pipe_info is not None:
            pipes_bits[job_name] = pipe_info
        tpl_fname = jobs.get_default_template_fname(dest_dir, job_name)
        tpl_dir = op.dirname(tpl_fname)
        if not op.exists(tpl_dir):
            os.makedirs(tpl_dir)
        with open(tpl_fname, 'w') as fp:
            fp.write(conf)
        jobs_templates[job_name] = tpl_fname
    return pipes_bits, jobs_templates


def _write_jobs_defs(jobs_templates, dest_dir):
    fname = jobs.get_jobs_defs_fname(dest_dir)
    text = jobs.format_default_jobs_defs(jobs_templates, dest_dir)
    with open(fname, 'w') as fp:
        fp.write(text)


def _write_pipelines(pipes_bits, dest_dir):
    fname = pipelines.get_fname(dest_dir)
    text = pipelines.format_pipes_bits(pipes_bits)
    with open(fname, 'w') as fp:
        fp.write(text)


def _write_default_context(dest_dir):
    fname = jobs.get_default_context_fname(dest_dir)
    open(fname, 'w').close()
