import os
import os.path as op

import configobj
from . import repository


def get_local_conf_fname():
    return op.expanduser(op.join('~', '.config', 'jenskipper.conf'))


def get_local_conf():
    fname = get_local_conf_fname()
    dirname = op.dirname(fname)
    if not op.exists(dirname):
        os.makedirs(dirname)
    return configobj.ConfigObj(fname)


def get_repository_conf():
    base_dir = repository.search_base_dir()
    if base_dir is not None:
        fname = repository.get_conf_fname(base_dir)
        return configobj.ConfigObj(fname)
    else:
        return {}


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
    keys = list(path)
    while keys:
        key = keys.pop(0)
        obj = obj[key]
    return obj


def set(path, value, in_repos=True):
    if in_repos:
        obj = conf = get_repository_conf()
    else:
        obj = conf = get_local_conf()
    keys = list(path)
    while keys:
        key = keys.pop(0)
        if not keys:
            obj[key] = value
        else:
            try:
                obj = obj[key]
            except KeyError:
                obj[key] = {}
                obj = obj[key]
    conf.write()
