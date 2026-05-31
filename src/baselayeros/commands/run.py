import json
from typing import Any, Dict

import click
import requests


@click.command(help="Run an action against the local BaseLayerOS substrate.")
@click.argument("action_id")
@click.option("--payload", default="{}", help="JSON payload string.")
@click.option("--subject", default="demo-user", help="Identity subject.")
@click.option("--role", "roles", multiple=True, default=["analyst"], help="Identity roles.")
@click.option("--port", default=8000, help="Substrate port.")
def run(action_id: str, payload: str, subject: str, roles: Any, port: int):
    try:
        payload_obj: Dict[str, Any] = json.loads(payload)
    except json.JSONDecodeError:
        raise click.ClickException("Invalid JSON for --payload")

    identity = {"subject": subject, "roles": list(roles)}

    click.echo("Submitting governed action:")
    click.echo(f"  action:   {action_id}")
    click.echo(f"  identity: {identity}")
    click.echo(f"  payload:  {payload_obj}")

    url = f"http://localhost:{port}/execute"
    try:
        resp = requests.post(
            url,
            json={
                "action": action_id,
                "payload": payload_obj,
                "identity": identity,
            },
            timeout=10,
        )
    except requests.RequestException as e:
        raise click.ClickException(f"Failed to reach substrate: {e}") from e

    if resp.status_code != 200:
        raise click.ClickException(f"Substrate error: {resp.status_code} {resp.text}")

    data = resp.json()
    click.echo("\nResult:")
    click.echo(json.dumps(data, indent=2))
