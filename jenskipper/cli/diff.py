import difflib
import sys

try:
    from lxml import etree  # NOQA
    HAVE_LXML = True
except ImportError:
    HAVE_LXML = False
import click

from . import decorators
from .. import utils
from .. import repository
from .. import jenkins_api
from .. import conf
from .. import jobs
from .. import exceptions


@click.command()
@decorators.repos_command
@decorators.jobs_command
@decorators.context_command
@decorators.handle_all_errors
def diff(jobs_names, base_dir, context_overrides):
    '''
    Show diffs between JOBS in the local repository and on the server.

    If no JOBS are specified, diff all jobs.
    '''
    if not HAVE_LXML:
        click.secho('This command works better if you install lxml:',
                    fg='yellow', bold=True)
        click.secho('  $ pip install lxml', fg='green')
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    for job_name in jobs_names:
        try:
            print_job_diff(base_dir, jenkins_url, job_name, context_overrides)
        except exceptions.JobNotFound:
            utils.sechowrap('')
            utils.sechowrap('Unknown job: %s' % job_name, fg='red', bold=True)
            utils.sechowrap('Job is present in the local repository, but not '
                            'on the Jenkins server.', fg='red')
            sys.exit(1)


def print_job_diff(base_dir, jenkins_url, job_name, context_overrides,
                   reverse=False):
    local_xml = repository.get_job_conf(base_dir, job_name, context_overrides)
    local_xml = _prepare_xml(local_xml)
    remote_xml, _ = jenkins_api.handle_auth(base_dir,
                                            jenkins_api.get_job_config,
                                            jenkins_url,
                                            job_name)
    remote_xml = _prepare_xml(remote_xml)
    from_text = remote_xml
    to_text = local_xml
    from_file = 'remote/%s.xml' % job_name
    to_file = 'local/%s.xml' % job_name
    if reverse:
        from_text, to_text = to_text, from_text
        from_file, to_file = to_file, from_file
    diff = difflib.unified_diff(from_text, to_text, fromfile=from_file,
                                tofile=to_file)
    _print_diff(diff)


def _prepare_xml(xml):
    xml = utils.format_xml(xml)
    xml = utils.unescape_xml(xml)
    xml = xml.replace('\r\n', '\n')
    _, xml = jobs.extract_hash_from_description(xml)
    return xml.splitlines(True)


def _print_diff(diff):
    for line in diff:
        if line.startswith('---') or line.startswith('+++'):
            click.secho(line, fg='white', bold=True, nl=False)
        elif line.startswith('-'):
            click.secho(line, fg='red', nl=False)
        elif line.startswith('+'):
            click.secho(line, fg='green', nl=False)
        else:
            click.secho(line, nl=False)
