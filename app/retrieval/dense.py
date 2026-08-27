import numpy as np
from sentence_transformers import SentenceTransformer

from app.models import Chunk, RetrievedChunk


class DenseRetriever:
    def __init__(self, chunks: list[Chunk], model_name: str):
        self.chunks = chunks
        self.model = SentenceTransformer(model_name)
        self.embeddings = self.model.encode(
            [chunk.text for chunk in chunks],
            normalize_embeddings=True,
        )

    def search(self, query: str, top_k: int) -> list[RetrievedChunk]:
        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
        )[0]

        scores = np.dot(self.embeddings, query_embedding)
        indices = np.argsort(scores)[::-1][:top_k]

        return [
            RetrievedChunk(
                chunk=self.chunks[int(idx)],
                score=float(scores[idx]),
                rank=rank,
            )
            for rank, idx in enumerate(indices, start=1)
        ]
