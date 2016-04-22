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
