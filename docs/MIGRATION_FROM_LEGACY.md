# Migration from Legacy Sources

The previous implementation kept duplicated weights in `common.py` and `demo_relevance.py`, ran only as local scripts, and applied a linear sum directly. Those legacy files have been removed after their responsibilities were migrated to the maintained platform.

## Migration map

- `src/create_theseus_ontology.py` -> `scripts/create_theseus_ontology.py`
- `src/common.py` -> `src/epm/ontology.py`, `src/epm/policies.py`, `src/epm/models.py`, and `src/epm/service.py`
- `src/demo_relevance.py` -> `src/epm/engine.py` and the `/v1/relevance` endpoint
- local example scripts -> two HTTP consumers in `clients/`
- `src/run_all_analyses.py` and `src/simulate_examples.py` -> `scripts/run_local_demo.py` and `pytest`

## Main corrections

1. Descriptor IDs were standardized in English.
2. Weights were removed from source code and placed in versioned JSON policies.
3. Provenance became mandatory.
4. Context is no longer represented as only a label.
5. Valuation, comparison, aggregation, interaction rules, and thresholds became explicit, versioned policy components.
6. Binary similarity received its own contract.
7. Results include explicit validity and identity warnings.
8. The API allows independent systems to consume the platform.
9. Observation values were separated from the stable ontology and made explicit in every request.
10. Typed OWL descriptor classes replaced free-form descriptor-kind strings.
