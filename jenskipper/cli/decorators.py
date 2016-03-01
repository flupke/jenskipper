import functools

import click

from .. import repository


def repos_command(func):
    '''
    Base options for repository commands.
    '''

    @click.option('--jk-dir', '-d', default='.', help='Location of the '
                  'jenskipper repository (default: the current directory).')
    @functools.wraps(func)
    def wrapper(jk_dir, **kwargs):
        base_dir = repository.check_dir_is_in_repository(jk_dir)
        return func(base_dir=base_dir, **kwargs)

    return wrapper
