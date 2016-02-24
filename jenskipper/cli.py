import click

from .import_ import import_


@click.group()
def main():
    '''
    Pilot Jenkins from the command line.
    '''


main.add_command(import_)
