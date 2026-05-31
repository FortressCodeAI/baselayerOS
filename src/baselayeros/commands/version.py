import click
from baselayeros import __version__
from baselayeros.cli.colours import info


@click.command(help="Show BaseLayerOS version")
def version():
    click.echo(info(f"BaseLayerOS CLI version {__version__}"))
