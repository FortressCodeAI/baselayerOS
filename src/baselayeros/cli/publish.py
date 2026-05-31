import typer
import requests

app = typer.Typer()

@app.command()
def publish(pack_id: str):
    url = f"http://localhost:8000/api/publish/{pack_id}"
    r = requests.post(url)
    if r.status_code != 200:
        typer.echo(f"Error: {r.text}")
        raise typer.Exit(code=1)

    data = r.json()
    typer.echo(f"Published: {data['pack_id']}")
    typer.echo(f"Remaining GIUs: {data['remaining_gius']}")
