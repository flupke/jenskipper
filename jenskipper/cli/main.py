import click

from .import_ import import_
from .show import show


@click.group()
def main():
    '''
    Pilot Jenkins from the command line.
    '''


main.add_command(import_)
main.add_command(show)
