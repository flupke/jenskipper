import uuid

import click

from . import decorators
from . import build
from .. import conf
from .. import jenkins_api
from .. import repository


@click.command()
@decorators.repos_command
@decorators.jobs_command
@decorators.context_command
@decorators.handle_conf_errors
def test(jobs_names, base_dir, context_overrides):
    '''
    Create temporary copies of JOBS and execute them.

    This command blocks until all jobs are done. Jobs that succeeded are
    deleted, and failures are kept for inspection.
    '''
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    new_jobs_names, jenkins_url = _create_temp_jobs(jobs_names,
                                                    base_dir,
                                                    jenkins_url,
                                                    context_overrides)
    queue_urls, jenkins_url = build.trigger_builds(new_jobs_names, base_dir,
                                                   jenkins_url)
    results = build.wait_for_jobs(queue_urls, jenkins_url)
    _process_results(results, jenkins_url)


def _create_temp_jobs(jobs_names, base_dir, jenkins_url, context_overrides):
    ret = []
    for job_name in jobs_names:
        temp_name = '%s.%s' % (job_name, uuid.uuid4().hex[:8])
        conf = repository.get_job_conf(base_dir, job_name,
                                       context_overrides=context_overrides)
        _, jenkins_url = jenkins_api.handle_auth(base_dir,
                                                 jenkins_api.push_job_config,
                                                 jenkins_url,
                                                 temp_name,
                                                 conf)
        ret.append(temp_name)
    return ret, jenkins_url


def _process_results(results, jenkins_url):
    for job_name, (job_url, result) in results.items():
        orig_job_name, _, _ = job_name.rpartition('.')
        if result == 'SUCCESS':
            jenkins_api.delete_job(jenkins_url, job_name)
            suffix = ''
        else:
            suffix = ', see %s' % job_url
        build.print_job_result(orig_job_name, result, suffix)