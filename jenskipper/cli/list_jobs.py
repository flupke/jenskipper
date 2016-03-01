import sys

import click

from .. import repository


@click.command('list-jobs')
@click.option('--jk-dir', '-d', default='.', help='Location of the jenskipper '
              'repository (default: the current directory).')
def list_jobs(jk_dir):
    '''
    List jobs in a repository.
    '''
    base_dir = repository.search_base_dir(jk_dir)
    if base_dir is None:
        click.secho('Could not find a jenskipper repository in "%s" and its '
                    'parent directories' % jk_dir, fg='red', bold=True)
        sys.exit(1)
    jobs_defs = repository.get_jobs_defs(base_dir)
    for name in sorted(jobs_defs):
        print name
