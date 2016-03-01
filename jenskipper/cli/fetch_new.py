import click

from . import decorators
from . import import_
from .. import repository
from .. import conf
from .. import jenkins_api


@click.command('fetch-new')
@decorators.repos_command
def fetch_new(base_dir):
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    repos_jobs = repository.get_jobs_defs(base_dir)
    server_jobs, jenkins_url = jenkins_api.handle_auth(base_dir,
                                                       jenkins_api.list_jobs,
                                                       jenkins_url)
    new_jobs = set(server_jobs).difference(repos_jobs)
    if new_jobs:
        with click.progressbar(new_jobs, label='Fetching new jobs') as bar:
            pipes_bits, jobs_templates = import_.write_jobs_templates(
                base_dir,
                jenkins_url,
                bar
            )
        import_.write_jobs_defs(base_dir, jobs_templates, 'a', pad_lines=1)
        import_.write_pipelines(base_dir, pipes_bits, 'a')
    else:
        click.secho('No new jobs')
