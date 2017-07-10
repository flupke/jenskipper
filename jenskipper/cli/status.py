import click
import requests
import sys

from . import decorators
from .. import jenkins_api
from .. import conf
from .. import utils


JOB_STATUS = (
    ('lastStableBuild', 'Last stable: %s', 'stable'),
    ('lastFailedBuild', 'Last failed: %s', 'failed'),
    ('lastUnstableBuild', 'Last unstable: %s', 'unstable'),
)


@click.command('status')
@click.argument('job_name')
@decorators.repos_command
@decorators.handle_all_errors()
def get_job_status(base_dir, job_name):
    """
    Retrieve the status of a job.
    """
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    try:
        job_data, jenkins_url = jenkins_api.handle_auth(base_dir,
                                                        jenkins_api.get_object,
                                                        jenkins_url,
                                                        '/job/%s' % job_name)
    except requests.HTTPError as exc:
        if exc.response.status_code == 404:
            utils.sechowrap('Unkown job: %s' % job_name)
        else:
            utils.sechowrap('Unexpected HTTP error %s while trying to '
                            'retrieve job data' % exc.response.status_code,
                            fg='red')
        sys.exit(1)

    if job_data['lastCompletedBuild'] is None:
        print 'Job was never built'
        sys.exit(0)

    last_completed_build = job_data['lastCompletedBuild']['number']

    last_jobs_lines = []
    for key, fmt, status in JOB_STATUS:
        build_data = job_data[key]
        if build_data is not None:
            last_jobs_lines.append(fmt % build_data['number'])
            if last_completed_build == job_data[key]['number']:
                print 'Status: %s' % status

    print 'Last completed: %s' % last_completed_build
    print '\n'.join(last_jobs_lines)
