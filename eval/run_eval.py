import json
import statistics
from pathlib import Path

from app.config import get_settings
from app.pipeline import RAGPipeline


def reciprocal_rank(source: str, citations) -> float:
    for rank, citation in enumerate(citations, start=1):
        if citation.source == source:
            return 1.0 / rank
    return 0.0


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0

    values = sorted(values)
    index = min(len(values) - 1, round((len(values) - 1) * p))
    return values[index]


def main():
    dataset = json.loads(
        Path("eval/dataset.json").read_text(encoding="utf-8")
    )
    pipeline = RAGPipeline(get_settings())

    hit_count = 0
    mrr_total = 0.0
    keyword_scores = []
    latencies = []

    for row in dataset:
        result = pipeline.ask(
            question=row["question"],
            department=row.get("department"),
        )

        sources = [c.source for c in result.citations]
        hit_count += int(row["expected_source"] in sources)
        mrr_total += reciprocal_rank(
            row["expected_source"],
            result.citations,
        )

        answer = result.answer.lower()
        keywords = row["expected_keywords"]
        matched = sum(1 for keyword in keywords if keyword.lower() in answer)
        keyword_scores.append(matched / len(keywords))
        latencies.append(result.latency_ms)

        print(f"\nQ: {row['question']}")
        print(f"A: {result.answer}")
        print(f"Sources: {sources}")
        print(f"Trace: {result.trace_id}")

    total = len(dataset)

    print("\n--- Summary ---")
    print(f"Hit@K: {hit_count / total:.3f}")
    print(f"MRR: {mrr_total / total:.3f}")
    print(f"Keyword coverage: {sum(keyword_scores) / total:.3f}")
    print(f"P50 latency: {statistics.median(latencies):.1f} ms")
    print(f"P95 latency: {percentile(latencies, 0.95):.1f} ms")


if __name__ == "__main__":
    main()
