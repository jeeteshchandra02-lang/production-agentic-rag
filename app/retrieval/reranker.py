from sentence_transformers import CrossEncoder

from app.models import RetrievedChunk


class Reranker:
    def __init__(self, model_name: str):
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        candidates: list[RetrievedChunk],
        top_k: int,
    ) -> list[RetrievedChunk]:
        if not candidates:
            return []

        pairs = [(query, item.chunk.text) for item in candidates]
        scores = self.model.predict(pairs)

        ranked = sorted(
            zip(candidates, scores),
            key=lambda item: float(item[1]),
            reverse=True,
        )[:top_k]

        return [
            RetrievedChunk(
                chunk=item.chunk,
                score=float(score),
                rank=rank,
            )
            for rank, (item, score) in enumerate(ranked, start=1)
        ]
