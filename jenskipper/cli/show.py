import click

from . import decorators
from .. import repository
from .. import jobs


@click.command()
@click.argument('job_name')
@decorators.repos_command
def show(job_name, base_dir):
    '''
    Show the rendered XML of JOB_NAME.
    '''
    jobs_defs = repository.get_jobs_defs(base_dir)
    pipelines = repository.get_pipelines(base_dir)
    job_def = jobs_defs[job_name]
    pipe_info = pipelines.get(job_name)
    print jobs.render_job(job_def, pipe_info, base_dir)
