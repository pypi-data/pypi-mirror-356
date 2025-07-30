import click

from mosamatic.tasks import selectl3


@click.group()
def cli():
    pass


cli.add_command(selectl3.selectl3)