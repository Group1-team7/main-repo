# Limitations

- Deterministic keyword rules can miss risks or create false positives.
- The MVP supports pasted text only; it does not parse PDFs.
- The local JSONL knowledge base contains placeholders until manually verified.
- No vector database, Neo4j, fine-tuning, or model-based legal reasoning is included.
- The chat is scoped to contract risk summaries and refuses legal-advice requests.
- The MVP does not produce a final legal conclusion.

TODO[PERSON-2]: Add known segmentation and rule failures after testing real samples.
TODO[PERSON-3]: Add backend and guardrail residual risks after integration testing.
