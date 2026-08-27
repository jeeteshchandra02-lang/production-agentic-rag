from collections import defaultdict

from app.models import RetrievedChunk


def reciprocal_rank_fusion(
    result_sets: list[list[RetrievedChunk]],
    k: int = 60,
) -> list[RetrievedChunk]:
    scores = defaultdict(float)
    chunks = {}

    for results in result_sets:
        for item in results:
            chunk_id = item.chunk.id
            chunks[chunk_id] = item.chunk
            scores[chunk_id] += 1.0 / (k + item.rank)

    ranked_ids = sorted(scores, key=scores.get, reverse=True)

    return [
        RetrievedChunk(
            chunk=chunks[chunk_id],
            score=scores[chunk_id],
            rank=rank,
        )
        for rank, chunk_id in enumerate(ranked_ids, start=1)
    ]
