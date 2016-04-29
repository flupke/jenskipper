import os
import os.path as op

import click

from . import decorators
from .. import repository


@click.command()
@click.option('--delete/--no-delete', default=False, help='Delete '
              'unused templates.')
@decorators.repos_command
@decorators.handle_all_errors()
def sweep(base_dir, delete):
    '''
    Find unused templates in the current repository.
    '''
    # Get dead templates list and print it
    jobs_defs = repository.get_jobs_defs(base_dir)
    defs_templates = set(d['template'] for d in jobs_defs.values())
    templates_dir = repository.get_templates_dir(base_dir)
    top_level_files = set(n for n in os.listdir(templates_dir)
                          if (op.isfile(op.join(templates_dir, n)) and
                              not n.startswith('.')))
    dead_files = top_level_files.difference(defs_templates)
    print '\n'.join(sorted(dead_files))

    # Optionally delete dead templates
    if delete:
        for basename in dead_files:
            path = op.join(templates_dir, basename)
            os.unlink(path)
