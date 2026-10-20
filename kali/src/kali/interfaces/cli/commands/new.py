import shutil
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parents[2] / "templates"

def new_project(name: str):
    project = Path(name)

    if project.exists():
        print(f"❌ Directory '{name}' already exists.")
        return

    project.mkdir()
    for item in TEMPLATE_DIR.iterdir():
        dest = project / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy(item, dest)

    print(f"🎉 Created governed Kali project: {name}")
