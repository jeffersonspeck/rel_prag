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

The suite also checks the exact contexts, agents, vectors, and scores from Equations 10-13, rejects incomplete observations and empty provenance, enforces the normalized threshold decision in Equation 18, preserves formal descriptor order, and verifies that audit events retain the complete Equation 23 evaluation configuration.

The final PDF was reviewed both through text extraction and rendered pages 14-23. Equation numbering and the computational assumptions in Section 7.3 were checked against the rendered document.
