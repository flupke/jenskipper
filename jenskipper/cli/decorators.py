import functools
import sys

import click

from .. import repository
from .. import conf
from .. import exceptions


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


def handle_conf_errors(func):
    '''
    Print nice error messages on configuration validation errors.
    '''
    # TODO: find more DRY way to handle these exceptions

    @functools.wraps(func)
    def wrapper(**kwargs):
        try:
            return func(**kwargs)
        except exceptions.ConfError as exc:
            conf.print_validation_errors(exc.conf,
                                         exc.validation_results)
            sys.exit(1)

    return wrapper
