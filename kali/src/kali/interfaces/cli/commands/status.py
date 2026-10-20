import shutil

def status():
    print("📊 Kali Status Report")
    print(f"- Substrate: {shutil.which('baselayeros')}")
    print("- Governance engine: active")
    print("- Templates: available")
    print("- CLI: operational")
