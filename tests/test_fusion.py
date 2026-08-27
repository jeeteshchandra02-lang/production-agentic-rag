from app.models import Chunk, RetrievedChunk
from app.retrieval.fusion import reciprocal_rank_fusion


def make_result(chunk_id: str, rank: int):
    chunk = Chunk(
        id=chunk_id,
        source="doc.md",
        text=f"text for {chunk_id}",
        position=0,
    )
    return RetrievedChunk(chunk=chunk, score=1.0, rank=rank)


def test_rrf_rewards_results_seen_by_multiple_retrievers():
    dense = [make_result("a", 1), make_result("b", 2)]
    lexical = [make_result("b", 1), make_result("c", 2)]

    fused = reciprocal_rank_fusion([dense, lexical])

    assert fused[0].chunk.id == "b"
