import click

from .. import repository
from .. import jobs


@click.command()
@click.argument('job_name')
@click.option('--jk-dir', '-d', default='.', help='Location of the jenskipper '
              'repository (default: the current directory).')
def show(job_name, jk_dir):
    '''
    Show the rendered XML of JOB_NAME.
    '''
    jobs_defs = repository.get_jobs_defs(jk_dir)
    pipelines = repository.get_pipelines(jk_dir)
    job_def = jobs_defs[job_name]
    pipe_info = pipelines.get(job_name, None)
    print jobs.render_job(job_def, pipe_info, jk_dir)
