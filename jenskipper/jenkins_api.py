import urlparse
import urllib

import click
import requests
import re

from . import conf
from . import exceptions


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

    Raise a :class:`jenskipper.exceptions.JobTypeMismatch` error if the job
    type being pushed does not match the server-side job type (e.g. trying to
    push a multi-configuration job on a freestyle job).
    '''
    url = _get_job_config_url(jenkins_url, name)
    resp = requests.post(url, config)
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        if exc.response.status_code == 500:
            match = re.search('java.io.IOException: Expecting class '
                              '([^\d\W][\w.]*) but got class ([^\d\W][\w.]*) '
                              'instead', exc.response.text)
            if match is not None:
                expected_type, pushed_type = match.groups()
                raise exceptions.JobTypeMismatch(expected_type, pushed_type)
        raise


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


def delete_job(jenkins_url, name):
    '''
    Delete job named *name* on server at *jenkins_url*.
    '''
    url = urlparse.urljoin(jenkins_url, '/job/%s/doDelete' % name)
    resp = requests.post(url)
    resp.raise_for_status()


def rename_job(jenkins_url, name, new_name):
    '''
    Rename job *name* to *new_name* on server at *jenkins_url*.
    '''
    url = urlparse.urljoin(jenkins_url,
                           '/job/%s/doRename?newName=%s' % (name, new_name))
    resp = requests.post(url)
    resp.raise_for_status()


def create_job(jenkins_url, name, conf):
    '''
    Create a new job named *name* with *conf* on server at *jenkins_url*.
    '''
    url = urlparse.urljoin(jenkins_url, '/createItem?name=%s' %
                           urllib.quote_plus(name))
    resp = requests.post(url, conf,
                         headers={'Content-Type': 'application/xml'})
    resp.raise_for_status()
