import sys

import click

from . import decorators
from . import diff
from .. import repository
from .. import jobs
from .. import jenkins_api
from .. import conf
from .. import utils


@click.command()
@click.option('--force/--no-force', default=False, help='Allow pushing, even '
              'if pushes are disabled in the configuration.')
@click.option('--allow-overwrite/--no-allow-overwrite', default=False,
              help='Allow overwriting changes made in the GUI.')
@decorators.repos_command
@decorators.jobs_command
@decorators.handle_conf_errors
def push(jobs_names, base_dir, force, allow_overwrite):
    '''
    Push JOBS to the current repository. Push all jobs if nothing is specified.
    '''
    _check_push_flag(base_dir, force)
    jenkins_url = conf.get(base_dir, ['server', 'location'])
    jobs_defs = repository.get_jobs_defs(base_dir)
    pipelines = repository.get_pipelines(base_dir)
    _check_for_gui_modifications(base_dir, jenkins_url, jobs_names,
                                 allow_overwrite)
    with click.progressbar(jobs_names, label='Pushing jobs') as bar:
        _push_jobs(base_dir, jenkins_url, pipelines, bar, jobs_defs)


def _check_for_gui_modifications(base_dir, jenkins_url, jobs_names,
                                 allow_overwrite):
    if allow_overwrite:
        return
    gui_was_modified = False
    for job_name in jobs_names:
        conf, jenkins_url = jenkins_api.handle_auth(
            base_dir,
            jenkins_api.get_job_config,
            jenkins_url,
            job_name
        )
        saved_hash, conf = jobs.extract_hash_from_description(conf)
        actual_hash = jobs.get_conf_hash(conf)
        if saved_hash is not None and saved_hash != actual_hash:
            utils.sechowrap('It looks like job "%s" has been modified in the '
                            'Jenkins GUI:' % job_name, fg='red', bold=True)
            utils.sechowrap('')
            diff.print_job_diff(base_dir, jenkins_url, job_name, reverse=True)
            utils.sechowrap('')
            gui_was_modified = True
    if gui_was_modified:
        utils.sechowrap('You can force push the jobs with the '
                        '--allow-overwrite flag', fg='red')
        sys.exit(1)


def _push_jobs(base_dir, jenkins_url, pipelines, jobs_names, jobs_defs):
    templates_dir = repository.get_templates_dir(base_dir)
    for job_name in jobs_names:
        job_def = jobs_defs[job_name]
        pipe_info = pipelines.get(job_name)
        final_conf = jobs.render_job(job_def, pipe_info, templates_dir,
                                     insert_hash=True)
        _, jenkins_url = jenkins_api.handle_auth(base_dir,
                                                 jenkins_api.push_job_config,
                                                 jenkins_url,
                                                 job_name,
                                                 final_conf)


def _check_push_flag(base_dir, force):
    if force or not conf.get(base_dir, ['server', 'forbid_push']):
        return
    utils.sechowrap('Pushes are not allowed for this repository', fg='red',
                    bold=True)
    utils.sechowrap('')
    utils.sechowrap('The push command is explicitely disabled for this '
                    'repository. This usually means that pushes are done '
                    'server-side with a SCM hook.', fg='red')
    utils.sechowrap('')
    utils.sechowrap('If you really know what you\'re doing, you can use the '
                    '--force flag to push anyway.', fg='red')
    sys.exit(1)
