import click
import tarfile
from pathlib import Path
from baselayeros.cli.utils import load_json
from baselayeros.cli.colors import success


@click.command(help="Package a module into a deterministic artifact")
@click.argument("name")
def package(name):
    module_path = Path(".baselayeros/modules") / name
    metadata = load_json(module_path / "module.json")

    artifact = Path(".baselayeros/artifacts") / f"{metadata['name']}-{metadata['version']}.tar.gz"

    with tarfile.open(artifact, "w:gz") as tar:
        tar.add(module_path, arcname=name)

    click.echo(success(f"Packaged: {artifact}"))
