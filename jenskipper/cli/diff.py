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
@click.argument('job_name')
@decorators.repos_command
def diff(job_name, base_dir):
    '''
    Show diff between JOB in the repository and on the server.
    '''
    if not HAVE_LXML:
        click.secho('This command works better if you install lxml:',
                    fg='yellow', bold=True)
        click.secho('pip install lxml', fg='green')
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    local_xml = repository.get_job_conf(base_dir, job_name)
    local_xml = _prepare_xml(local_xml)
    remote_xml, _ = jenkins_api.handle_auth(base_dir,
                                            jenkins_api.get_job_config,
                                            jenkins_url,
                                            job_name)
    remote_xml = _prepare_xml(remote_xml)
    diff = difflib.unified_diff(remote_xml, local_xml, fromfile='remote',
                                tofile='local')
    print ''.join(diff)


def _prepare_xml(xml, unescape=False):
    xml = utils.format_xml(xml)
    xml = utils.unescape_xml(xml)
    xml = xml.replace('\r\n', '\n')
    return xml.splitlines(True)
