import click
import requests

from .. import jenkins_api
from .. import conf
from . import decorators


@click.command('auth')
@decorators.repos_command
def authenticate(base_dir):
    """
    Authenticate against the jenkins server.
    """
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    jenkins_api.handle_auth(base_dir, _open_home, jenkins_url)


def _open_home(jenkins_url):
    response = requests.get(jenkins_url)
    response.raise_for_status()
