from rank_bm25 import BM25Okapi

from app.models import Chunk, RetrievedChunk
from app.utils import tokenize


class BM25Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        corpus = [tokenize(chunk.text) for chunk in chunks]
        self.index = BM25Okapi(corpus)

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        scores = self.index.get_scores(tokenize(query))
        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True,
        )[:top_k]

        return [
            RetrievedChunk(
                chunk=self.chunks[idx],
                score=float(score),
                rank=rank,
            )
            for rank, (idx, score) in enumerate(ranked, start=1)
        ]
