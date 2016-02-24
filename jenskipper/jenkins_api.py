import urlparse

import requests


def list_jobs(jenkins_url):
    '''
    Get the names of jobs on the *jenkins_url* server.
    '''
    url = urlparse.urljoin(jenkins_url, '/api/json')
    resp = requests.get(url)
    data = resp.json()
    return [j['name'] for j in data['jobs']]


def get_job_config(jenkins_url, name):
    '''
    Get the XML configuration for job *name* in *jenkins_url*.
    '''
    url = urlparse.urljoin(jenkins_url, '/job/%s/config.xml' % name)
    resp = requests.get(url)
    return resp.text
