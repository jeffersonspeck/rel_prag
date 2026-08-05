# Technical Validation

The delivered version was verified with:

```bash
PYTHONPATH=src pytest -q
python -m compileall -q src clients scripts tests
PYTHONPATH=src python scripts/run_local_demo.py
```

Test-suite result:

```text
17 passed
```

A local Uvicorn server was also started, and both HTTP consumers were executed:

```text
navigation-v1   -> unary_contextual_relevance
preservation-v1 -> unary_contextual_relevance
```

Both systems used the same entity and descriptive state, but returned different values because they applied different contextual policies.

The suite checks the repository's structured contexts, the exact Equation 10-11 Ship vectors and published scores, and the Equation 12-13 geographic calculation. It also rejects incomplete observations and empty provenance, enforces normalized threshold decisions, preserves formal descriptor order, and verifies that audit events retain the complete evaluation configuration.

The supplied 14-page PDF was reviewed through full text extraction and rendered page images. Its SHA-256 is `7D659806C8989E74661B113818ACA16C70C8D946D3F1F5F523164288FA9FD9C0`. The review confirmed Equations 1-14 and also established that the supplied article has no Equations 15-23 and no Section 7.3.
