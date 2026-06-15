import click # type: ignore
from pathlib import Path
import shutil


@click.command(help="Create a new blueprint")
@click.argument("name")
def create_blueprint(name):
    src = Path(__file__).parent.parent / "templates" / "blueprint" / "blueprint.json"
    dst = Path(".baselayeros/blueprints") / f"{name}.json"
    dst.parent.mkdir(exist_ok=True)

    shutil.copy(src, dst)
    dst.write_text(dst.read_text().replace("{{name}}", name))

    click.echo(f"Created blueprint: {dst}")
