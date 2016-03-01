import click

from .. import repository


@click.command('list-jobs')
@click.option('--jk-dir', '-d', default='.', help='Location of the jenskipper '
              'repository (default: the current directory).')
def list_jobs(jk_dir):
    '''
    List jobs in a repository.
    '''
    base_dir = repository.check_dir_is_in_repository(jk_dir)
    jobs_defs = repository.get_jobs_defs(base_dir)
    for name in sorted(jobs_defs):
        print name
