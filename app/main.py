from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.ask import router as ask_router
from app.api.ingest import router as ingest_router

app = FastAPI(title="RAGdoll")

app.include_router(health_router)
app.include_router(ask_router)
app.include_router(ingest_router)