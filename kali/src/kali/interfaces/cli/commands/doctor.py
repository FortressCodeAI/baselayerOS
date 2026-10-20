import shutil
import sys
from pathlib import Path

def doctor():
    print("🩺 Running Kali diagnostics...\n")

    checks = {
        "Python Version": sys.version,
        "Substrate Installed": shutil.which("baselayeros"),
        "Template Directory": str(Path(__file__).parents[2] / "templates"),
    }

    for key, value in checks.items():
        print(f"{key}: {value}")

    print("\n✅ Diagnostics complete.")
