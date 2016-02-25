import click

from .. import jobs


@click.command()
@click.argument('job_name')
def show(job_name):
    '''
    Show the rendered XML of JOB_NAME
    '''
