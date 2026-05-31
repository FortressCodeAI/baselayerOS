import click # type: ignore
import json
from pathlib import Path

from baselayeros.credits.billing import Billing


# Explicit group object so Pylance recognizes .command
giu = click.Group(help="GIU ledger, balances, burns, and revenue transparency")


# ------------------------------------------------------------
# BALANCE
# ------------------------------------------------------------
@giu.command("balance")
@click.argument("account_id")
def giu_balance(account_id):
    billing = Billing()
    bal = billing.balance(account_id)
    click.echo(f"GIU balance for {account_id}: {bal}")


# ------------------------------------------------------------
# HISTORY
# ------------------------------------------------------------
@giu.command("history")
@click.argument("account_id")
def giu_history(account_id):
    ledger = Path(".baselayeros/giu_ledger.jsonl")
    if not ledger.exists():
        click.echo("No ledger found")
        return

    with ledger.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            if rec["account_id"] == account_id:
                click.echo(json.dumps(rec, indent=2))


# ------------------------------------------------------------
# BURNS
# ------------------------------------------------------------
@giu.command("burns")
@click.option("--account", default=None)
@click.option("--action", default=None)
def giu_burns(account, action):
    ledger = Path(".baselayeros/giu_ledger.jsonl")
    audit = Path(".baselayeros/audit.log")

    if not ledger.exists():
        click.echo("No ledger found")
        return

    # Load audit envelopes for action filtering
    audit_map = {}
    if audit.exists():
        with audit.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                env = json.loads(line)
                audit_map[env["audit_id"]] = env

    with ledger.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)

            if rec["direction"] != "debit":
                continue

            if account and rec["account_id"] != account:
                continue

            if action:
                env = audit_map.get(rec["audit_id"])
                if not env or env["action"] != action:
                    continue

            click.echo(json.dumps(rec, indent=2))


# ------------------------------------------------------------
# BUILDER REVENUE
# ------------------------------------------------------------
@giu.command("revenue")
@click.argument("builder_id")
def giu_revenue(builder_id):
    ledger = Path(".baselayeros/giu_ledger.jsonl")
    if not ledger.exists():
        click.echo("No ledger found")
        return

    total = 0
    with ledger.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            if rec["account_id"] == builder_id and rec["direction"] == "credit":
                total += rec["amount"]

    click.echo(f"Builder revenue for {builder_id}: {total} GIUs")


# ------------------------------------------------------------
# TRACE
# ------------------------------------------------------------
@giu.command("trace")
@click.argument("audit_id")
def giu_trace(audit_id):
    ledger = Path(".baselayeros/giu_ledger.jsonl")
    audit = Path(".baselayeros/audit.log")

    if not ledger.exists() or not audit.exists():
        click.echo("Missing ledger or audit log")
        return

    # Find ledger entries
    burns = []
    with ledger.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            if rec["audit_id"] == audit_id:
                burns.append(rec)

    # Find audit envelope
    envelope = None
    with audit.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            env = json.loads(line)
            if env["audit_id"] == audit_id:
                envelope = env
                break

    click.echo("=== Ledger Entries ===")
    for b in burns:
        click.echo(json.dumps(b, indent=2))

    click.echo("\n=== Audit Envelope ===")
    if envelope:
        click.echo(json.dumps(envelope, indent=2))
    else:
        click.echo("No audit envelope found")
