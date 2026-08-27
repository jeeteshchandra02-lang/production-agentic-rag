from pydantic import BaseModel, Field


class Chunk(BaseModel):
    id: str
    source: str
    text: str
    position: int
    metadata: dict[str, str] = Field(default_factory=dict)


class RetrievedChunk(BaseModel):
    chunk: Chunk
    score: float
    rank: int


class AskRequest(BaseModel):
    question: str
    department: str | None = None


class Citation(BaseModel):
    source: str
    chunk_id: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieved_chunks: int
    latency_ms: float
    trace_id: str
