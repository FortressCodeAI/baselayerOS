from pathlib import Path
import json
import shutil
from datetime import datetime

from .verification import verify_pack
from .ledger import burn_gius
from .registry import load_registry, save_registry

ROOT = Path(__file__).resolve().parents[2]
PACKS_DIR = ROOT / "Standard" / "packs"
REGISTRY_DIR = ROOT / "Demo" / "registry" / "published"

PUBLISH_COST = 100  # demo only

def publish_pack(pack_id: str, builder_id: str = "james"):
    # 1. Load canonical pack
    pack_path = PACKS_DIR / f"{pack_id}.json"
    if not pack_path.exists():
        raise ValueError(f"Pack not found: {pack_id}")

    pack = json.loads(pack_path.read_text())

    # 2. Verification
    verify_pack(pack)

    # 3. Burn GIUs
    burn_gius(builder_id, PUBLISH_COST)

    # 4. Move pack to published registry
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(pack_path, REGISTRY_DIR / f"{pack_id}.json")

    # 5. Update registry metadata
    registry = load_registry()
    registry[pack_id] = {
        "status": "published",
        "published_at": datetime.utcnow().isoformat(),
        "giu_cost": PUBLISH_COST,
    }
    save_registry(registry)

    return {
        "pack_id": pack_id,
        "status": "published",
        "remaining_gius": burn_gius(builder_id, 0, dry_run=True),
    }
