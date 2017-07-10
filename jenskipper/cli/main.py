import click

from .import_ import import_
from .show import show
from .push import push
from .list_jobs import list_jobs
from .fetch_new import fetch_new
from .diff import diff
from .build import build
from .prune import prune
from .test import test
from .sweep import sweep
from .log import log
from .patch import patch
from .dirty import print_dirty_jobs
from .get_artifact import get_artifact


@click.group()
def main():
    '''
    Pilot Jenkins from the command line.
    '''


main.add_command(import_)
main.add_command(show)
main.add_command(push)
main.add_command(list_jobs)
main.add_command(fetch_new)
main.add_command(diff)
main.add_command(build)
main.add_command(prune)
main.add_command(test)
main.add_command(sweep)
main.add_command(log)
main.add_command(patch)
main.add_command(print_dirty_jobs)
main.add_command(get_artifact)
