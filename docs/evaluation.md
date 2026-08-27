# Evaluation notes

The evaluation harness is intentionally small and easy to inspect.

## Retrieval metrics

### Hit@K

Checks whether the expected document appears in the retrieved context.

### MRR

Rewards the expected source more when it appears higher in the ranking.

## Generation check

Keyword coverage is used as a basic deterministic regression check in local
mode. It is not a semantic quality metric.

## Latency

The script reports P50 and P95 end-to-end latency. Model initialization is not
included in per-request latency once the pipeline is already loaded.

## What I would add next

- precision/recall over labeled chunks
- nDCG
- faithfulness evaluation
- answer relevance
- citation correctness
- adversarial prompt set
- retrieval tests with similar-but-wrong documents
