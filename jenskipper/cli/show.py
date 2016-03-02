import click

from . import decorators
from .. import repository


@click.command()
@click.argument('job_name')
@decorators.repos_command
def show(job_name, base_dir):
    '''
    Show the rendered XML of JOB_NAME.
    '''
    print repository.get_job_conf(base_dir, job_name)
