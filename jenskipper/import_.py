import os
import os.path as op
import sys

import click

from . import jenkins_api
from . import job_config
from . import pipelines


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
    jobs = jenkins_api.list_jobs(jenkins_url)
    with click.progressbar(jobs) as bar:
        pipe_bits = _save_templates(bar, dest_dir, jenkins_url)
    pipes_fname = pipelines.get_fname(dest_dir)
    pipes_text = pipelines.format_pipe_bits(pipe_bits)
    with open(pipes_fname, 'w') as fp:
        fp.write(pipes_text)


def _save_templates(jobs, dest_dir, jenkins_url):
    pipe_bits = {}
    for job_name in jobs:
        config = jenkins_api.get_job_config(jenkins_url, job_name)
        pipe_info, conf = job_config.extract_pipeline_conf(config)
        if pipe_info is not None:
            pipe_bits[job_name] = pipe_info
        conf_fname = job_config.get_default_template_fname(dest_dir,
                                                           job_name)
        conf_dir = op.dirname(conf_fname)
        if not op.exists(conf_dir):
            os.makedirs(conf_dir)
        with open(conf_fname, 'w') as fp:
            fp.write(conf)
    return pipe_bits
