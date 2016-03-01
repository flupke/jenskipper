import click

from .import_ import import_
from .show import show
from .list_jobs import list_jobs


@click.group()
def main():
    '''
    Pilot Jenkins from the command line.
    '''


main.add_command(import_)
main.add_command(show)
main.add_command(list_jobs)
