import click # type: ignore
from pathlib import Path
import shutil


@click.command(help="Create a new BaseLayerOS module")
@click.argument("name")
def create(name):
    src = Path(__file__).parent.parent / "templates" / "module"
    dst = Path(".baselayeros/modules") / name

    if dst.exists():
        raise click.ClickException("Module already exists")

    shutil.copytree(src, dst)

    # Replace placeholders
    for file in dst.rglob("*"):
        if file.is_file():
            text = file.read_text()
            text = text.replace("{{name}}", name)
            file.write_text(text)

    click.echo(f"Created module: {dst}")
