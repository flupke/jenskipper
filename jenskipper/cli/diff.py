import difflib

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


@click.command()
@click.argument('jobs_names', metavar='JOBS', nargs=-1)
@decorators.repos_command
def diff(jobs_names, base_dir):
    '''
    Show diffs between JOBS in the local repository and on the server.
    '''
    if not HAVE_LXML:
        click.secho('This command works better if you install lxml:',
                    fg='yellow', bold=True)
        click.secho('pip install lxml', fg='green')
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    if not jobs_names:
        jobs_names = repository.get_jobs_defs(base_dir)
    for job_name in jobs_names:
        _print_job_diff(base_dir, jenkins_url, job_name)


def _print_job_diff(base_dir, jenkins_url, job_name):
    local_xml = repository.get_job_conf(base_dir, job_name)
    local_xml = _prepare_xml(local_xml)
    remote_xml, _ = jenkins_api.handle_auth(base_dir,
                                            jenkins_api.get_job_config,
                                            jenkins_url,
                                            job_name)
    remote_xml = _prepare_xml(remote_xml)
    diff = difflib.unified_diff(remote_xml,
                                local_xml,
                                fromfile='remote/%s.xml' % job_name,
                                tofile='local/%s.xml' % job_name)
    _print_diff(diff)


def _prepare_xml(xml, unescape=False):
    xml = utils.format_xml(xml)
    xml = utils.unescape_xml(xml)
    xml = xml.replace('\r\n', '\n')
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
