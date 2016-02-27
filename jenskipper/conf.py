import os
import os.path as op

import configobj
from . import repository


def get_local_conf_fname():
    return op.expanduser(op.join('~', '.config', 'jenskipper.conf'))


def get_local_conf(create_dir=False):
    fname = get_local_conf_fname()
    if create_dir:
        dirname = op.dirname(fname)
        if not op.exists(dirname):
            os.makedirs(dirname)
    return configobj.ConfigObj(fname)


def get_repository_conf():
    base_dir = repository.search_base_dir()
    fname = repository.get_conf_fname(base_dir)
    return configobj.ConfigObj(fname)


def get_conf():
    '''
    Return the actual conf.

    It is built by merging the repository conf into the local conf.
    '''
    local_conf = get_local_conf()
    repos_conf = get_repository_conf()
    local_conf.merge(repos_conf)
    return local_conf


def get(path):
    obj = get_conf()
    keys = path.split('.')
    while keys:
        key = keys.pop(0)
        obj = obj[key]
    return obj


def set(path, value):
    obj = conf = get_conf()
    keys = path.split('.')
    while keys:
        key = keys.pop(0)
        if not keys:
            obj[key] = value
        else:
            obj = obj[key]
    conf.write()
