import click # type: ignore
from pathlib import Path
from baselayeros.cli.colours import success


@click.command(help="Initialize a BaseLayerOS workspace")
def init():
    root = Path(".baselayeros")
    root.mkdir(exist_ok=True)

    (root / "modules").mkdir(exist_ok=True)
    (root / "artifacts").mkdir(exist_ok=True)
    (root / "env.json").write_text("{}")

    click.echo(success("Initialized BaseLayerOS workspace"))
