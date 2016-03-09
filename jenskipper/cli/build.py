import click

from . import decorators
from .. import jenkins_api
from .. import conf


@click.command()
@decorators.repos_command
@decorators.jobs_command
@decorators.handle_conf_errors
def build(jobs_names, base_dir):
    '''
    Build JOBS immediately.
    '''
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    for name in jobs_names:
        jenkins_api.handle_auth(
            base_dir,
            jenkins_api.build_job,
            jenkins_url,
            name
        )
