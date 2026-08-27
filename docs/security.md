# Security notes

The current version adds two small controls to make the learning project more
realistic.

## Prompt-injection check

A lightweight rule-based check blocks obvious attempts to override hidden
instructions. This is not a complete defense. I added it mostly to make the
security boundary explicit and to have something concrete to test.

A production version would combine:
- input classification
- strict tool schemas
- retrieval authorization
- output validation
- audit logging
- human approval for high-risk actions

## Metadata filtering

Chunks can contain a `department` tag. The API accepts an optional department
and filters retrieval results before fusion/reranking.

This is only an example of access-scoped retrieval. In a real multi-tenant
system the filter must come from authenticated identity/authorization context,
not directly from user input.
