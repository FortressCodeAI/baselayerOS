from pathlib import Path

KALI_HOME = Path.home() / ".kali"

CONFIG_FILE = KALI_HOME / "config.json"
LICENSE_FILE = KALI_HOME / "license.json"
AUTH_FILE = KALI_HOME / "auth.json"


def ensure_home():

    KALI_HOME.mkdir(parents=True, exist_ok=True)
