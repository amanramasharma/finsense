# RAG module

This package implements retrieval-augmented generation for explanations.

- `retrieval/`: vector + keyword search over OpenSearch with filters (symbol, time, source).
- `orchestration/`: glue code that combines retrieval + LLM prompts and guardrails.
- `postprocessing/`: ranking, deduplication, snippet extraction, and response formatting.