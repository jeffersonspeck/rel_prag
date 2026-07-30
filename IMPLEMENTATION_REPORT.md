# Implementation Report

## Objective

Transform the previous scripts into a reusable platform with a stable ontology, versioned external policies, a computational engine, an API, and two independent consumers.

## Problems corrected from the previous source files

1. **Duplicated weights**: profiles appeared in more than one module. Each policy now exists only once in `data/policies/`.
2. **Text-only provenance**: `ProvenanceRecord` is now mandatory and returned with every decision.
3. **Context represented as a label**: context now includes a goal, time scope, environment, roles, and norms.
4. **Rigid linear sum**: replaceable aggregators and interaction rules are now available.
5. **Conflated relevance and similarity**: each now has a separate contract, endpoint, and response.
6. **Risk of treating similarity as identity**: the continuity field is operational, and the API never claims numerical identity.
7. **Local execution only**: external systems can now consume the model over HTTP.
8. **No audit trail**: every evaluation now creates a JSONL record.
9. **No integration contract**: the exported OpenAPI contract is available at `docs/openapi.json`.
10. **Limited testability**: an automated suite covers the ontology, policies, aggregation, similarity, and API.

## Two implemented consumers

### Navigation Operations System

- selects `navigation-v1`;
- uses the same ship state and ontology;
- prioritizes structure and the disposition to navigate;
- demonstrates a joint requirement between descriptors.

### Heritage Preservation System

- selects `preservation-v1`;
- uses the same ship state and ontology;
- prioritizes origin, historical value, and the monument role;
- receives different explanations and provenance.

## Deliberately unresolved matters

- universal weight elicitation;
- empirical validation of the vectors;
- automatic negotiation between policies;
- a theory of numerical identity;
- global transitivity of continuity;
- complete execution of the calculation in OWL.

These items are documented as limitations and are not presented as implemented capabilities.
