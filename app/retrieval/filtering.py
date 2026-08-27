from app.models import RetrievedChunk


def filter_by_department(
    results: list[RetrievedChunk],
    department: str | None,
) -> list[RetrievedChunk]:
    if not department:
        return results

    filtered = [
        item
        for item in results
        if item.chunk.metadata.get("department") in {"", None, department}
    ]

    return [
        RetrievedChunk(
            chunk=item.chunk,
            score=item.score,
            rank=rank,
        )
        for rank, item in enumerate(filtered, start=1)
    ]
