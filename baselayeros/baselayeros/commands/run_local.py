import click
import json
from baselayeros.server import SubstrateServer
from baselayeros.cli.colours import success, error


@click.command(name="run-local", help="Run a module action locally")
@click.argument("action")
@click.option("--payload", default="{}", help="JSON payload")
def run_local(action, payload):
    server = SubstrateServer()

    request = {
        "action": action,
        "payload": json.loads(payload),
        "subject_id": "local-dev",
        "roles": ["developer"],
        "state": {},
        "request_id": "cli-run",
    }

    result = server.execute(request)
    click.echo(json.dumps(result, indent=2))
