# Design decisions

## Keep the first version synchronous

The first goal was to compare retrieval behavior and evaluation results. I would
make external model calls asynchronous before adding real concurrent traffic.

## Do not hide retrieval behind one framework abstraction

BM25, dense retrieval, fusion and reranking are separate Python components.
That makes it easier to test ranking behavior and swap one stage at a time.

## Use a local answer fallback

The fallback means a reviewer can clone and run most of the project without
credentials. It is deliberately basic and is not presented as an LLM.

## Keep query rewriting conservative

Aggressive rewriting can remove exact names and IDs that BM25 needs. The first
version only normalizes whitespace. LLM-based rewriting is something I would
add only after measuring it on the evaluation set.
