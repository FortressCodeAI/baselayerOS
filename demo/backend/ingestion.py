from pathlib import Path
import json
from typing import List, Dict

ROOT = Path(__file__).resolve().parents[2]
PACKS_DIR = ROOT / "Standard" / "packs"

class PackIngestionError(Exception):
    pass

def discover_pack_files() -> List[Path]:
    if not PACKS_DIR.exists():
        raise PackIngestionError(f"Pack directory not found: {PACKS_DIR}")
    return sorted(PACKS_DIR.glob("*.json"))

def load_pack_file(path: Path) -> Dict:
    try:
        return json.loads(path.read_text())
    except Exception as e:
        raise PackIngestionError(f"Failed to load pack {path.name}: {e}") from e

def basic_pack_validation(pack: Dict, filename: str) -> None:
    required_top = ["meta", "io", "workflow", "governance"]
    for key in required_top:
        if key not in pack:
            raise PackIngestionError(f"{filename}: missing required section '{key}'")

    if "id" not in pack["meta"]:
        raise PackIngestionError(f"{filename}: meta.id is required")

    wf = pack["workflow"]
    if "states" not in wf or "transitions" not in wf:
        raise PackIngestionError(f"{filename}: workflow.states/transitions required")

def ingest_all_packs() -> Dict[str, Dict]:
    """
    Returns a dict: { pack_id: pack_dict }
    """
    packs: Dict[str, Dict] = {}
    for path in discover_pack_files():
        pack = load_pack_file(path)
        basic_pack_validation(pack, path.name)
        pack_id = pack["meta"]["id"]
        packs[pack_id] = pack
    return packs
