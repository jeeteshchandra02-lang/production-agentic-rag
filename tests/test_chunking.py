from app.ingestion import chunk_text


def test_chunk_text_creates_multiple_chunks():
    text = ("This is a sentence. " * 100).strip()

    chunks = chunk_text(
        text=text,
        source="test.md",
        chunk_size=180,
        overlap=30,
    )

    assert len(chunks) > 1
    assert chunks[0].source == "test.md"
    assert chunks[0].id == "test-0"


def test_chunk_text_ignores_empty_input():
    assert chunk_text("", "empty.md", 200, 20) == []
