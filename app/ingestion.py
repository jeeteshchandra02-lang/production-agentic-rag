from pathlib import Path

from app.models import Chunk
from app.utils import normalize_whitespace


def chunk_text(
    text: str,
    source: str,
    chunk_size: int,
    overlap: int,
    metadata: dict[str, str] | None = None,
) -> list[Chunk]:
    text = normalize_whitespace(text)
    if not text:
        return []

    metadata = metadata or {}
    chunks = []
    start = 0
    position = 0

    while start < len(text):
        end = min(len(text), start + chunk_size)
        part = text[start:end]

        if end < len(text):
            boundary = part.rfind(". ")
            if boundary > chunk_size // 2:
                end = start + boundary + 1
                part = text[start:end]

        chunks.append(
            Chunk(
                id=f"{Path(source).stem}-{position}",
                source=source,
                text=part.strip(),
                position=position,
                metadata=metadata,
            )
        )

        if end == len(text):
            break

        start = max(0, end - overlap)
        position += 1

    return chunks


def _metadata_from_path(path: Path) -> dict[str, str]:
    # The sample project uses the top-level folder as a simple department tag.
    parts = path.parts
    if "sample_docs" in parts:
        idx = parts.index("sample_docs")
        if idx + 1 < len(parts) - 1:
            return {"department": parts[idx + 1]}

    return {}


def load_documents(directory: str, chunk_size: int, overlap: int) -> list[Chunk]:
    root = Path(directory)
    chunks = []

    for path in sorted(root.rglob("*")):
        if path.suffix.lower() not in {".txt", ".md"}:
            continue

        chunks.extend(
            chunk_text(
                text=path.read_text(encoding="utf-8"),
                source=path.name,
                chunk_size=chunk_size,
                overlap=overlap,
                metadata=_metadata_from_path(path),
            )
        )

    return chunks
