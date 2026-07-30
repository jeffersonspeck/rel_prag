# Epistemic-Pragmatic Model Platform

Reference implementation of the model presented in **The Ship of Theseus Paradox and Epistemic-Pragmatic Weighting in Ontological Modeling**.

The project reflects the conceptual and formal corrections introduced in the final version:

- separation between the stable ontology `S(I)` and external policies `W(A,C)`;
- structured context represented as `C=<g,t,e,r,n>`;
- explicit provenance represented as `Pi_W=<source, method, evidence, timestamp, version>`;
- explicit separation between the descriptor schema `S(I)` and observed values `v_I(p_i)`;
- distinction between unary relevance `Rel_prag(I,A,C)` and binary similarity `Sim_prag(I',I'',A,C)`;
- thresholded similarity treated as support for operational continuity, never as numerical identity;
- versioned valuation, comparison, aggregation, interaction, and threshold settings;
- a shared API consumed by two independent external systems;
- an audit trail and policy versioning.

## Architecture

```text
Stable RDF/OWL ontology
        |
        v
Epistemic-Pragmatic Model API
        |
        +-----------------------------+
        |                             |
Navigation Operations System   Heritage Preservation System
policy=navigation-v1           policy=preservation-v1
```

Both consumers submit **the same ship state** and use **the same ontology**. They differ in their explicit policy, agent, and context. Neither consumer modifies the ontology.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows
pip install -e ".[dev]"
python scripts/create_theseus_ontology.py
```

## Run the API

```bash
uvicorn epm.api:app --reload
```

API entry point: `http://127.0.0.1:8000/`

Interactive documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Run the two consumer systems

In separate terminals, while keeping the API running:

```bash
python clients/navigation_system.py
python clients/heritage_system.py
```

Both consume `POST /v1/relevance`, but select different policies.

## Run the example without HTTP

```bash
python scripts/run_local_demo.py
```

The command creates `output/demo_results.json`, containing results for both systems and an additional binary-similarity example.

## Tests

```bash
pytest
```

The tests verify:

- the absence of weights, agents, and observation defaults from the stable ontology;
- explicit OWL types for the heterogeneous descriptors;
- compatibility between policies and descriptors;
- meaningful context and provenance;
- the exact contexts, agents, vectors, and numerical results from Equations 10-13;
- complete observed state outside the ontology;
- requirement-aware aggregation;
- normalized scores before operational threshold decisions;
- reproducible audit records;
- the distinction between operational similarity and numerical identity;
- the API's HTTP contract.

## Known limitations

This implementation does not provide:

- a metaphysical theory of numerical identity;
- a universal method for eliciting weights;
- automatic negotiation between incompatible policies;
- empirical validation of the illustrative vectors;
- complete inference of numerical operations by an OWL reasoner.

The ontology represents the stable vocabulary and structure. Calculations, provenance, auditing, and contextual decisions are performed externally in the application layer.

## Documentation index

Every Markdown document in the repository is listed below.

| Document | Purpose |
| --- | --- |
| [`README.md`](README.md) | Project overview, quick start, validation commands, limitations, and documentation index. |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history linking implementation changes and regression tests to the article's formal definitions and equations. |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Top-level copy of the architecture and design decisions for convenient access. |
| [`IMPLEMENTATION_REPORT.md`](IMPLEMENTATION_REPORT.md) | Top-level copy of the implementation report and the problems addressed by the current platform. |
| [`REVIEW_CHANGES.md`](REVIEW_CHANGES.md) | Top-level copy mapping review observations to concrete implementation changes and remaining limitations. |
| [`docs/API_USAGE.md`](docs/API_USAGE.md) | Example requests and response semantics for the relevance and similarity endpoints. |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Canonical description of the ontology, policy, engine, and integration layers. |
| [`docs/FORMALIZATION_MAPPING.md`](docs/FORMALIZATION_MAPPING.md) | Equation-by-equation mapping from the final article PDF to code, tests, complexity assumptions, and declared boundaries. |
| [`docs/IMPLEMENTATION_REPORT.md`](docs/IMPLEMENTATION_REPORT.md) | Canonical implementation report, including the two consumers and deliberately unresolved questions. |
| [`docs/MIGRATION_FROM_LEGACY.md`](docs/MIGRATION_FROM_LEGACY.md) | Migration map from the removed legacy scripts to the maintained package, API, clients, and tests. |
| [`docs/REVIEW_CHANGES.md`](docs/REVIEW_CHANGES.md) | Canonical response to conceptual and technical review observations. |
| [`docs/TWO_SYSTEMS.md`](docs/TWO_SYSTEMS.md) | Explanation of how two independent systems consume the same ontology and API with different policies. |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | Commands and observed results used to validate the implementation. |
