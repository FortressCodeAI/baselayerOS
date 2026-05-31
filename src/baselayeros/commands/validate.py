import click
import json
from pathlib import Path
import requests

from baselayeros.audit import AuditLog, canonical_json, sha256_hex  # noqa: F401
from baselayeros.runtime.loader import load_all_modules, load_all_packs


@click.command(name="validate", help="Run full governance validation across BaseLayerOS.")
@click.option("--port", default=8000, show_default=True, help="Substrate port.")
def validate(port: int):
    click.secho("🔍 Running governance validation...", fg="cyan")

    # ------------------------------------------------------------
    # 1. Audit chain integrity
    # ------------------------------------------------------------
    audit_path = Path(".baselayeros/audit.log")
    audit_log = AuditLog(audit_path)

    if audit_log.verify_chain():
        click.secho("✓ Audit chain integrity verified", fg="green")
    else:
        click.secho("❌ Audit chain is BROKEN", fg="red")

    # ------------------------------------------------------------
    # 2. GIU ledger integrity
    # ------------------------------------------------------------
    ledger_path = Path(".baselayeros/giu_ledger.jsonl")
    if ledger_path.exists():
        try:
            with ledger_path.open("r", encoding="utf-8") as f:
                for line in f:
                    json.loads(line)
            click.secho("✓ GIU ledger is valid JSONL", fg="green")
        except Exception:
            click.secho("❌ GIU ledger is corrupted", fg="red")
    else:
        click.secho("⚠ GIU ledger missing (may be fresh install)", fg="yellow")

    # ------------------------------------------------------------
    # 3. Module manifest validation
    # ------------------------------------------------------------
    try:
        modules = load_all_modules()
        click.secho(f"✓ Loaded {len(modules)} modules", fg="green")
    except Exception as e:
        click.secho("❌ Module loading failed", fg="red")
        click.echo(repr(e))

    # ------------------------------------------------------------
    # 4. Pack manifest validation
    # ------------------------------------------------------------
    try:
        packs = load_all_packs()
        click.secho(f"✓ Loaded {len(packs)} packs", fg="green")
    except Exception as e:
        click.secho("❌ Pack loading failed", fg="red")
        click.echo(repr(e))

    # ------------------------------------------------------------
    # 5. Substrate health check
    # ------------------------------------------------------------
    try:
        resp = requests.get(f"http://localhost:{port}/docs", timeout=2)
        if resp.status_code == 200:
            click.secho("✓ Substrate is reachable", fg="green")
        else:
            click.secho("❌ Substrate returned unexpected status", fg="red")
    except Exception:
        click.secho("❌ Substrate is NOT reachable", fg="red")

    # ------------------------------------------------------------
    # 6. Identity key integrity
    # ------------------------------------------------------------
    key_path = Path.home() / ".baselayeros/key"
    if key_path.exists() and key_path.stat().st_size == 32:
        click.secho("✓ Signing identity key is valid", fg="green")
    else:
        click.secho("❌ Signing identity key is missing or invalid", fg="red")

    click.secho("\nGovernance validation complete.", fg="cyan")
