# Production Agentic RAG

A production-style RAG project I built while learning what changes when a basic
"retrieve and answer" demo is pushed closer to a real application.

The project focuses on retrieval quality, reranking, grounded generation,
evaluation and a small API layer. I intentionally kept the UI out of scope.

## What I wanted to learn

A vector-only RAG flow is easy to build, but it can struggle with:
- exact terms, IDs and product names
- questions that need more than one piece of context
- semantically similar chunks that do not actually answer the question
- answers that sound right but are not well grounded

This project experiments with hybrid retrieval and reranking to improve that.

## Flow

```text
User question
     |
     v
Query normalization
     |
     v
+-------------------------+
| Hybrid retrieval        |
| - dense embeddings      |
| - BM25 lexical search   |
+-------------------------+
     |
     v
Reciprocal Rank Fusion
     |
     v
Cross-encoder reranking
     |
     v
Top context
     |
     v
LLM / local fallback
     |
     v
Answer + source citations
```

## Features

- local Markdown/text document ingestion
- chunking with overlap
- dense retrieval with sentence-transformers
- BM25 lexical retrieval
- reciprocal-rank fusion (RRF)
- cross-encoder reranking
- grounded answer generation
- source citations
- metadata-aware retrieval filtering
- basic prompt-injection checks
- per-request trace IDs
- FastAPI endpoint
- small retrieval/generation evaluation harness
- unit tests
- Dockerfile
- GitHub Actions CI

## Repository structure

```text
production-agentic-rag/
├── app/
│   ├── api.py
│   ├── config.py
│   ├── ingestion.py
│   ├── llm.py
│   ├── models.py
│   ├── pipeline.py
│   ├── retrieval/
│   │   ├── bm25.py
│   │   ├── dense.py
│   │   ├── fusion.py
│   │   └── reranker.py
│   └── utils.py
├── data/sample_docs/
├── docs/
├── eval/
├── tests/
├── .github/workflows/ci.yml
├── Dockerfile
└── requirements.txt
```

## Run locally

```bash
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

The default provider is `local`, which keeps the project runnable without an
API key. To use OpenAI for generation:

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your-key
```

Start the API:

```bash
uvicorn app.api:app --reload
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/ask   -H "Content-Type: application/json"   -d '{"question":"What is the refund policy for enterprise subscriptions?"}'
```

## Evaluation

The current evaluation script measures:
- Hit@K
- MRR
- answer keyword coverage
- end-to-end latency

```bash
python -m eval.run_eval
```

The dataset is intentionally small. I use it as a regression check while
changing retrieval parameters rather than treating it as a benchmark.

## Why hybrid retrieval?

Dense embeddings are good for semantic similarity, but enterprise questions
often contain exact identifiers and uncommon names. BM25 provides a useful
lexical signal, so combining both helps with recall.

## Why RRF?

Dense search and BM25 scores have different meanings and ranges. RRF combines
rankings instead of trying to normalize two unrelated score distributions.

## Why rerank?

The first retrieval stage is optimized for recall. The cross-encoder is more
expensive, so it only runs over a small candidate set and decides which chunks
are most useful for the exact question.

## Current limitations

- vector embeddings are rebuilt on process startup
- no persistent vector database yet
- query rewriting is intentionally conservative
- no metadata filters or tenant authorization yet
- evaluation dataset is small

## Next things I want to try

- persistent Qdrant/pgvector index
- persistent Qdrant/pgvector index
- async model calls
- structured tracing
- LLM-as-a-judge evaluation
- prompt-injection regression tests
- tenant-aware authorization before retrieval
- multi-hop query decomposition
