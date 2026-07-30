# Technical Validation

The delivered version was verified with:

```bash
PYTHONPATH=src pytest -q
python -m compileall -q src clients scripts tests
PYTHONPATH=src python scripts/run_local_demo.py
```

Test-suite result:

```text
15 passed
```

A local Uvicorn server was also started, and both HTTP consumers were executed:

```text
navigation-v1   -> unary_contextual_relevance
preservation-v1 -> unary_contextual_relevance
```

Both systems used the same entity and descriptive state, but returned different values because they applied different contextual policies.

The suite also checks the exact illustrative vectors and scores from the article, rejects incomplete observations and empty provenance, enforces normalized threshold decisions, and verifies that audit events preserve the complete evaluation configuration.
