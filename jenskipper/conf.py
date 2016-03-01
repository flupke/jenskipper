import os
import os.path as op

import configobj
from . import repository


def get_user_conf_fname():
    return op.expanduser(op.join('~', '.config', 'jenskipper.conf'))


def get_user_conf():
    '''
    Get the global user configuration.

    Return a :class:`configobj.ConfigObj` object.
    '''
    fname = get_user_conf_fname()
    dirname = op.dirname(fname)
    if not op.exists(dirname):
        os.makedirs(dirname)
    return configobj.ConfigObj(fname)


def get_repository_conf(base_dir):
    '''
    Get the configuration for repository in *base_dir*.

    Return a :class:`configobj.ConfigObj` object.
    '''
    fname = repository.get_conf_fname(base_dir)
    return configobj.ConfigObj(fname)


def get_conf(base_dir):
    '''
    Get the actual configuration, built by merging the repository conf into the
    global user conf.
    '''
    user_conf = get_user_conf()
    repos_conf = get_repository_conf(base_dir)
    user_conf.merge(repos_conf)
    return user_conf


def get(base_dir, path):
    obj = get_conf(base_dir)
    keys = list(path)
    while keys:
        key = keys.pop(0)
        obj = obj[key]
    return obj


def _set(conf, path, value):
    obj = conf
    keys = list(path)
    while keys:
        key = keys.pop(0)
        if not keys:
            obj[key] = value
        else:
            obj = obj.setdefault(key, {})
    conf.write()


def set_in_user(path, value):
    '''
    Write *value* in setting at *path*, in the global user configuration.
    '''
    conf = get_user_conf()
    _set(conf, path, value)


def set_in_repos(base_dir, path, value):
    '''
    Write *value* in setting at *path*, in the repository configuration in
    *base_dir*.
    '''
    conf = get_repository_conf(base_dir)
    _set(conf, path, value)
