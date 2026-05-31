from fastapi import FastAPI
from demo.backend.ingestion import ingest_all_packs

app = FastAPI()

PACK_REGISTRY = {}

def init_runtime():
    global PACK_REGISTRY
    PACK_REGISTRY = ingest_all_packs()

@app.on_event("startup")
def on_startup():
    init_runtime()
