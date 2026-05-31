import click
from pathlib import Path
from baselayeros.cli.colours import success, info


@click.group(help="Manage BaseLayerOS environments")
def env():
    pass


@env.command("list")
def env_list():
    env_file = Path(".baselayeros/env.json")
    click.echo(info(env_file.read_text()))
