import sys
import urlparse
import time

import requests
import click

from . import decorators
from .. import jenkins_api
from .. import conf
from .. import utils


RESULT_COLORS = {
    'SUCCESS': 'green',
    'UNSTABLE': 'yellow',
    'FAILURE': 'red',
}


@click.command()
@click.option('--block/--no-block', default=False, help='Block until builds '
              'are done and show their outcome.')
@decorators.repos_command
@decorators.jobs_command
@decorators.handle_conf_errors
def build(jobs_names, base_dir, block):
    '''
    Trigger builds for JOBS.
    '''
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    queue_urls = {}
    for name in jobs_names:
        queue_url, jenkins_url = jenkins_api.handle_auth(
            base_dir,
            jenkins_api.build_job,
            jenkins_url,
            name
        )
        queue_urls[name] = queue_url
    if block:
        _, username, password = utils.split_auth_in_url(jenkins_url)
        jobs_urls = _get_jobs_urls(queue_urls, username, password)
        if _wait_for_jobs(jobs_urls):
            sys.exit(1)


def _get_jobs_urls(queue_urls, username, password):
    ret = {}
    queue_urls = queue_urls.copy()
    while queue_urls:
        for job_name, queue_url in queue_urls.items():
            queue_url = utils.replace_auth_in_url(queue_url, username,
                                                  password)
            queue_url = urlparse.urljoin(queue_url, 'api/json')
            resp = requests.get(queue_url)
            if resp.status_code == 200:
                resp_dict = resp.json()
                if 'executable' in resp_dict:
                    job_url = resp_dict['executable']['url']
                    job_url = urlparse.urljoin(job_url, 'api/json')
                    job_url = utils.replace_auth_in_url(job_url, username,
                                                        password)
                    ret[job_name] = job_url
                    del queue_urls[job_name]
            elif resp.status_code == 404:
                # A 404 means that the queue info is not available anymore. We
                # don't have any way to tell if the job was executed or not in
                # this case, so just ignore it.
                utils.sechowrap('%s: unknown status' % job_name, fg='yellow')
                del queue_urls[job_name]
            else:
                resp.raise_for_status()
        time.sleep(1)
    return ret


def _wait_for_jobs(jobs_urls):
    jobs_urls = jobs_urls.copy()
    error = False
    while jobs_urls:
        for job_name, job_url in jobs_urls.items():
            resp = requests.get(job_url)
            resp.raise_for_status()
            resp_dict = resp.json()
            result = resp_dict['result']
            if result is not None:
                if result != 'SUCCESS':
                    error = True
                utils.sechowrap('%s: %s' % (job_name, result.lower()),
                                fg=RESULT_COLORS[result])
                del jobs_urls[job_name]
        time.sleep(1)
    return error
