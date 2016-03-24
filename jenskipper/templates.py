import traceback

import jinja2
import click

from . import utils


def render(templates_dir, template, context, context_overrides={}):
    '''
    Render a job XML from job definition.

    If *insert_hash* is true, also include a hash of the configuration as text
    in the job description.

    :param templates_dir: location of the jobs templates
    :param template: the path to the job template, relative to *templates_dir*
    :param context: a dict containing the variables passed to the tamplate
    :param context_overrides:
        a mapping that will be deep merged in the final context
    '''
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir),
                             autoescape=True,
                             undefined=jinja2.StrictUndefined)
    template = env.get_template(template)
    context = utils.deep_merge(context, context_overrides)
    return template.render(**context)


def extract_jinja_error(exc_info):
    '''
    Extract relevant informations from a Jinja2 exception.

    *exc_info* should be a ``(exc_type, exc_value, traceback)`` tuple, as
    returned by :func:`sys.exc_info`.

    Return a ``(title, stack, error)`` tuple, where *title* is the error title,
    *stack* a list of lines describing the stack that led to the error, and
    *error* the description of the error.

    Raise a :class:`TypeError` if the error is not a supported Jinja2 error.
    '''
    exc_type, exc_value, tb = exc_info
    if exc_type is jinja2.UndefinedError:
        title = u'Undefined variable encountered in template'
    elif exc_type is jinja2.TemplateSyntaxError:
        title = u'Syntax error in template'
    else:
        raise TypeError(exc_type)

    stack_lines = []
    jinja_tb = [x for x in traceback.extract_tb(tb)
                if x[2] in ('top-level template code', 'template')]
    for file_name, line, func_name, text in jinja_tb:
        stack_lines.append(u'  File "%s", line %s' % (file_name, line))
        stack_lines.append(u'    %s' % text)

    return title, stack_lines, unicode(exc_value)


def print_jinja_error(title, stack_lines, error):
    click.secho(title, fg='red', bold=True)
    click.secho('')
    for line in stack_lines:
        click.secho(line)
    click.secho('')
    click.secho(error, bold=True)
