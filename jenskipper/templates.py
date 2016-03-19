import jinja2

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
