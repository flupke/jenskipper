import functools
import sys

import click
import jinja2.exceptions
import yaml.error

from .. import repository
from .. import conf
from .. import exceptions
from .. import utils
from .. import templates


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


def jobs_command(func):
    '''
    Base options for jobs that take a list of jobs names.

    Expects a *base_dir* argument, so normally used after ``@repos_command``.
    '''

    @click.argument('jobs_names', metavar='JOBS', nargs=-1)
    @functools.wraps(func)
    def wrapper(jobs_names, base_dir, **kwargs):
        jobs_defs = repository.get_jobs_defs(base_dir)
        if not jobs_names:
            jobs_names = jobs_defs.keys()
        unknown_jobs = set(jobs_names).difference(jobs_defs)
        if unknown_jobs:
            click.secho('Unknown jobs: %s' % ', '.join(unknown_jobs), fg='red',
                        bold=True)
            sys.exit(1)
        return func(jobs_names=jobs_names, base_dir=base_dir, **kwargs)

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


def context_command(func):
    '''
    Base options for jobs that can override context variables on the command
    line.

    The command receives a *context_overrides* argument, a dict ready to be
    deep merged in templates contexts.
    '''

    @click.option('--context', '-c', 'context_vars', multiple=True,
                  metavar='VAR=VALUE', help='Override context VAR with '
                  'VALUE; use --context multiple times to override multiple '
                  'variables. Use dots to target a nested variable: '
                  'foo.bar=baz')
    @functools.wraps(func)
    def wrapper(context_vars, **kwargs):
        try:
            context_overrides = parse_context_vars(context_vars)
        except exceptions.MalformedContextVar as exc:
            click.secho('Malformed context var in command-line: %s' % exc,
                        fg='red', bold=True)
            sys.exit(1)
        return func(context_overrides=context_overrides, **kwargs)

    return wrapper


def parse_context_vars(context_vars):
    ret = {}
    for spec in context_vars:
        path, sep, value = spec.partition('=')
        if sep != '=':
            raise exceptions.MalformedContextVar(spec)
        path = path.split('.')
        utils.set_path_in_dict(ret, path, value, inplace=True)
    return ret


def handle_jinja_errors(func):
    '''
    Print nice error messages on jinja exceptions.

    Expect a *base_dir* argument, so normally used after ``@repos_command``.
    '''

    @functools.wraps(func)
    def wrapper(base_dir, **kwargs):
        try:
            return func(base_dir=base_dir, **kwargs)
        except jinja2.TemplateNotFound as exc:
            click.secho('Template not found: %s' % exc.name, fg='red',
                        bold=True)
        except jinja2.TemplateError:
            exc_info = sys.exc_info()
            stack, error = templates.extract_jinja_error(exc_info, base_dir)
            templates.print_jinja_error(stack, error)
        sys.exit(1)

    return wrapper


def handle_yaml_errors(func):
    '''
    Print nice error messages on yaml parse errors.
    '''

    @functools.wraps(func)
    def wrapper(**kwargs):
        try:
            return func(**kwargs)
        except yaml.error.MarkedYAMLError as exc:
            click.secho(u'YAML parser error: %s' % exc, fg='red', bold=True)
        sys.exit(1)

    return wrapper


def handle_all_errors(for_repos_command=True):
    '''
    Return a decorator that regroups all the error handling decorators.

    Set *for_repos_command* to false for commands not operating inside a
    Jenskipper repository.
    '''

    def decorator(func):
        if for_repos_command:

            @handle_conf_errors
            @handle_jinja_errors
            @handle_yaml_errors
            @functools.wraps(func)
            def wrapper(**kwargs):
                return func(**kwargs)

        else:

            @handle_conf_errors
            @handle_yaml_errors
            @functools.wraps(func)
            def wrapper(**kwargs):
                return func(**kwargs)

        return wrapper

    return decorator
