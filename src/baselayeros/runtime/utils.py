from pathlib import Path
import shutil


def reset_environment():
    root = Path(".baselayeros")

    ledger = root / "giu_ledger.jsonl"
    audit = root / "audit.log"
    modules_dir = root / "modules"
    packs_dir = root / "packs"

    if ledger.exists():
        ledger.unlink()
    if audit.exists():
        audit.unlink()
    if modules_dir.exists():
        shutil.rmtree(modules_dir)
    if packs_dir.exists():
        shutil.rmtree(packs_dir)

    root.mkdir(exist_ok=True)


def print_status(port: int, modules, packs, demo: bool):
    print("\n================ BaseLayerOS Status ================")
    print(f"Port: {port}")
    print(f"Modules loaded: {len(modules)}")
    print(f"Packs loaded: {len(packs)}")
    print(f"Demo mode: {'ON' if demo else 'OFF'}")
    print("====================================================")
