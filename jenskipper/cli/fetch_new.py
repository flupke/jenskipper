import sys

import click

from . import decorators
from . import import_
from .. import repository
from .. import conf
from .. import jenkins_api
from .. import exceptions
from .. import utils


@click.command('fetch-new')
@click.option('--force/--no-force', default=False, help='Allow overwriting '
              'existing files.')
@decorators.repos_command
@decorators.handle_all_errors()
def fetch_new(base_dir, force):
    '''
    Fetch new jobs in an existing repository.
    '''
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    repos_jobs = repository.get_jobs_defs(base_dir)
    server_jobs, jenkins_url = jenkins_api.handle_auth(base_dir,
                                                       jenkins_api.list_jobs,
                                                       jenkins_url)
    new_jobs = set(server_jobs).difference(repos_jobs)
    if new_jobs:
        try:
            with click.progressbar(new_jobs, label='Fetching new jobs') as bar:
                pipes_bits, jobs_templates = import_.write_jobs_templates(
                    base_dir,
                    jenkins_url,
                    bar,
                    allow_overwrite=force,
                )
        except exceptions.OverwriteError as exc:
            click.secho('File already exists: %s' % exc, fg='red',
                        bold=True)
            click.secho('Use --force to overwrite', fg='green')
            sys.exit(2)
        import_.write_jobs_defs(base_dir, jobs_templates, 'a', pad_lines=1)
        import_.write_pipelines(base_dir, pipes_bits, 'a')
    utils.print_jobs_list('New jobs:', new_jobs, empty_label='No new jobs',
                          fg='green')
