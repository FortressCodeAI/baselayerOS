import click
from pathlib import Path
from baselayeros.cli.colours import success, error


@click.command(help="Deploy a packaged module to the local substrate")
@click.argument("artifact")
def deploy(artifact):
    artifact_path = Path(".baselayeros/artifacts") / artifact

    if not artifact_path.exists():
        click.echo(error("Artifact not found"))
        raise click.Abort()

    click.echo(success(f"Deployed {artifact} to local substrate"))
