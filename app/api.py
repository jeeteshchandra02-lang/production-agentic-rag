from functools import lru_cache

from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.models import AskRequest, AskResponse
from app.pipeline import RAGPipeline


app = FastAPI(
    title="Production Agentic RAG",
    version="0.2.0",
)


@lru_cache
def get_pipeline() -> RAGPipeline:
    return RAGPipeline(get_settings())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    return get_pipeline().ask(
        question=request.question,
        department=request.department,
    )
