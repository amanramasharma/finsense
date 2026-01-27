# finsense

# NLP module

This package contains core text ML components for FinSense.

- `preprocessing/`: text cleaning, normalization, tokenization, language detection.
- `models/`: sentiment, topic/event, and entity-linking models.
- `pipelines/`: flows from raw text → enriched documents ready for embeddings and storage.

# RAG module

This package implements retrieval-augmented generation for explanations.

- `retrieval/`: vector + keyword search over OpenSearch with filters (symbol, time, source).
- `orchestration/`: glue code that combines retrieval + LLM prompts and guardrails.
- `postprocessing/`: ranking, deduplication, snippet extraction, and response formatting.
