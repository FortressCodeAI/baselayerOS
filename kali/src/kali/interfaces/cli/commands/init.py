import shutil
from pathlib import Path

TEMPLATE_DIR = Path(__file__).parents[2] / "templates"

def init_project():
    print("📦 Initializing Kali project in current directory...")

    for item in TEMPLATE_DIR.iterdir():
        dest = Path(".") / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy(item, dest)

    print("✅ Kali project initialized.")
