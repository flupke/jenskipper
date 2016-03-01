import sys

import click

from .. import repository
from .. import jobs
from .. import jenkins_api
from .. import conf


@click.command()
@click.argument('jobs_names', metavar='JOBS', nargs=-1)
@click.option('--jk-dir', '-d', default='.', help='Location of the jenskipper '
              'repository (default: the current directory).')
def push(jobs_names, jk_dir):
    '''
    Push JOBS to the current repository. Push all jobs if nothing is specified.
    '''
    base_dir = repository.check_dir_is_in_repository(jk_dir)
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    jobs_defs = repository.get_jobs_defs(base_dir)
    pipelines = repository.get_pipelines(base_dir)
    if not jobs_names:
        jobs_names = jobs_defs.keys()
    with click.progressbar(jobs_names, label='Pushing jobs') as bar:
        ret = _push_jobs(base_dir, jenkins_url, pipelines, bar, jobs_defs)
    sys.exit(ret)


def _push_jobs(base_dir, jenkins_url, pipelines, jobs_names, jobs_defs):
    ret = 0
    for job_name in jobs_names:
        if job_name not in jobs_defs:
            click.secho('unknown job: %s' % job_name, fg='red', bold=True)
            ret = 1
            continue
        job_def = jobs_defs[job_name]
        pipe_info = pipelines.get(job_name)
        final_conf = jobs.render_job(job_def, pipe_info, base_dir)
        jenkins_api.handle_auth(base_dir, jenkins_api.push_job_config,
                                jenkins_url, job_name, final_conf)
    return ret
