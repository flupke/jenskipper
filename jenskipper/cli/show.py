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
    base_dir = repository.check_dir_is_in_repository(jk_dir)
    jobs_defs = repository.get_jobs_defs(base_dir)
    pipelines = repository.get_pipelines(base_dir)
    job_def = jobs_defs[job_name]
    pipe_info = pipelines.get(job_name)
    print jobs.render_job(job_def, pipe_info, base_dir)
