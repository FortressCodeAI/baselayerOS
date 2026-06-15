import typer
from demo.backend.ingestion import ingest_all_packs, PackIngestionError

app = typer.Typer()

@app.command()
def validate():
    try:
        packs = ingest_all_packs()
    except PackIngestionError as e:
        typer.echo(f"[ERROR] {e}")
        raise typer.Exit(code=1)

    typer.echo(f"OK: {len(packs)} packs ingested and validated.")
    for pid in packs:
        typer.echo(f" - {pid}")
