# Architecture notes

## Retrieval path

The request enters `RAGPipeline.ask()`.

Dense and BM25 retrieval run independently. Their rankings are merged with
reciprocal-rank fusion. I keep a wider fused candidate list than the final
context size so the cross-encoder has enough candidates to compare.

Only the top reranked chunks are passed to answer generation.

## Failure modes I was trying to address

### Vector-only retrieval misses exact strings

Semantic embeddings are good at meaning, but enterprise questions often contain
invoice IDs, product names, error codes or policy names. BM25 gives those exact
terms more weight.

### Retrieval scores are not directly comparable

Dense search and BM25 scores have different ranges and meanings. RRF avoids
adding a made-up normalization rule and uses rank position instead.

### High recall does not mean good final context

The first-stage retrievers are intentionally broad. The cross-encoder is more
expensive but runs over only a small candidate set.

## Current limitation

The dense index is in memory and is rebuilt on startup. For a larger deployment
I would move embeddings into a persistent vector store and add metadata filters
before reranking.
