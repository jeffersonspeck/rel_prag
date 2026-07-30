# Implementation Report

## Objective

Transform the previous scripts into a reusable platform with a stable ontology, versioned external policies, a computational engine, an API, and two independent consumers.

## Problems corrected from the previous source files

1. **Duplicated weights**: profiles appeared in more than one module. Each policy now exists only once in `data/policies/`.
2. **Text-only provenance**: `ProvenanceRecord` is mandatory, non-empty, and returned with every decision.
3. **Context represented as a label**: context includes a non-empty goal, time scope, environment, roles, and norms.
4. **Rigid linear sum**: versioned aggregators and interaction rules are bound to the contextual policy.
5. **Conflated relevance and similarity**: each now has a separate contract, endpoint, and response.
6. **Risk of treating similarity as identity**: the continuity field is operational, and the API never claims numerical identity.
7. **Local execution only**: external systems can now consume the model over HTTP.
8. **No audit trail**: every evaluation creates a JSONL record containing the request, complete policy, and response.
9. **No integration contract**: the exported OpenAPI contract is available at `docs/openapi.json`.
10. **Limited testability**: an automated suite covers the ontology, policies, article vectors, published scores, valuation, aggregation, similarity, auditability, and API.

## Formalization alignment

- `S(I)` contains typed descriptor classes but no current or default observations.
- `v_I(p_i)` is produced from explicit request observations through versioned valuation rules.
- `W(A,C)` exactly reproduces the two illustrative vectors from the article.
- `Pi_W` requires source, method, evidence, timestamp, and version.
- each binary descriptor has an explicit comparison function `s_i`;
- `Agg_C`, interaction rules, and the operational threshold are selected by the policy rather than the caller;
- a threshold can only be applied to a normalized similarity score;
- audit events preserve every formal component needed to reproduce an evaluation.

## Two implemented consumers

### Navigation Operations System

- selects `navigation-v1`;
- uses the same ship state and ontology;
- prioritizes structure and the disposition to navigate;
- demonstrates a joint requirement between descriptors.
- keeps that requirement in the versioned navigation policy.

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
