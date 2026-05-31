import click # type: ignore
from pathlib import Path
import shutil


@click.command(help="Create a new action inside a module")
@click.argument("module")
@click.argument("action")
def create_action(module, action):
    module_path = Path(".baselayeros/modules") / module
    if not module_path.exists():
        raise click.ClickException("Module not found")

    src = Path(__file__).parent.parent / "templates" / "action" / "action.py"
    dst = module_path / f"{action}.py"

    shutil.copy(src, dst)

    text = dst.read_text()
    text = text.replace("{{class_name}}", action.title().replace("_", ""))
    text = text.replace("{{action_name}}", f"{module}.{action}")
    dst.write_text(text)

    click.echo(f"Created action: {dst}")
