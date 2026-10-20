import json
from pathlib import Path

CONFIG = Path.home() / ".kali_config.json"

def login():
    print("🔐 Kali Login")
    token = input("Enter your API token: ").strip()

    CONFIG.write_text(json.dumps({"api_token": token}, indent=2))
    print("✅ Token saved to ~/.kali_config.json")
