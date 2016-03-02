import urlparse

import click
import requests

from . import conf


def handle_auth(base_dir, func, jenkins_url, *args, **kwargs):
    '''
    Run an API function, handling authentication errors in an user-friendly
    way.

    *args* and *kwargs* are passed to *func*. Return a ``(ret, jenkins_url)``
    tuple, with *ret* the return value of *func* and *jenkins_url* the URL with
    correct auth bits in it.
    '''
    # Search auth in conf, unless it's contained in the URL
    canonical_url, username, password = split_auth(jenkins_url)
    if username is None and password is None:
        try:
            server_conf = conf.get(base_dir, [canonical_url])
        except KeyError:
            pass
        else:
            jenkins_url = _replace_auth(jenkins_url,
                                        server_conf['username'],
                                        server_conf['password'])

    # Try to execute decorated function, looping on auth errors
    user_gave_auth = False
    while True:
        try:
            ret = func(jenkins_url, *args, **kwargs)
            break
        except requests.HTTPError as exc:
            if exc.response.status_code == 401:
                jenkins_url = _get_credentials(jenkins_url)
                user_gave_auth = True
            else:
                raise

    # Propose to user to remember auth if he typed it
    if user_gave_auth:
        user_conf_fname = conf.get_user_conf_fname()
        if click.confirm('Save credentials in the global conf "%s"?' %
                         user_conf_fname):
            canonical_url, username, password = split_auth(jenkins_url)
            conf.set_in_user([canonical_url, 'username'], username)
            conf.set_in_user([canonical_url, 'password'], password)

    return (ret, jenkins_url)


def list_jobs(jenkins_url):
    '''
    Get the names of jobs on the *jenkins_url* server.
    '''
    url = urlparse.urljoin(jenkins_url, '/api/json')
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return [j['name'] for j in data['jobs']]


def _get_job_config_url(jenkins_url, name):
    return urlparse.urljoin(jenkins_url, '/job/%s/config.xml' % name)


def get_job_config(jenkins_url, name):
    '''
    Get the XML configuration for job *name* in *jenkins_url*.
    '''
    url = _get_job_config_url(jenkins_url, name)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text.encode('utf8')


def push_job_config(jenkins_url, name, config):
    '''
    Replace the configuration of job *name* at *jenkins_url* with *config* (a
    XML string).
    '''
    url = _get_job_config_url(jenkins_url, name)
    resp = requests.post(url, config)
    resp.raise_for_status()


def _get_credentials(jenkins_url):
    click.secho('Authorization error', fg='red', bold=True)
    click.secho('Please supply credentials to access %s' % jenkins_url)
    username = click.prompt('Username')
    password = click.prompt('Password', hide_input=True)
    click.secho('')
    return _replace_auth(jenkins_url, username, password)


def _replace_auth(url, username, password):
    parsed = urlparse.urlparse(url)
    hostport = _get_hostport(parsed)
    netloc = '%s:%s@%s' % (username, password, hostport)
    replaced = parsed._replace(netloc=netloc)
    return urlparse.urlunparse(replaced)


def _get_hostport(parsed_url):
    hostport = parsed_url.hostname
    if parsed_url.port is not None:
        hostport += ':%s' % parsed_url.port
    return hostport


def split_auth(url):
    '''
    Extract authentification bits from *url*.

    Return a ``(url_without_auth, username, password)`` tuple.
    '''
    parsed = urlparse.urlparse(url)
    hostport = _get_hostport(parsed)
    without_auth = parsed._replace(netloc=hostport)
    return urlparse.urlunparse(without_auth), parsed.username, parsed.password
