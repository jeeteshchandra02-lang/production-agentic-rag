from app.models import Chunk, RetrievedChunk
from app.retrieval.filtering import filter_by_department


def make_result(department: str, rank: int):
    chunk = Chunk(
        id=f"{department}-{rank}",
        source="doc.md",
        text="sample",
        position=0,
        metadata={"department": department},
    )
    return RetrievedChunk(chunk=chunk, score=1.0, rank=rank)


def test_department_filter():
    results = [
        make_result("billing", 1),
        make_result("security", 2),
    ]

    filtered = filter_by_department(results, "billing")

    assert len(filtered) == 1
    assert filtered[0].chunk.metadata["department"] == "billing"
