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

- Equations 1 and 9: `S(I)` contains typed descriptor classes but no current or default observations.
- Equation 3: each policy binds its vector to a complete `C=<g,t,e,r,n>`.
- Equation 5: `Pi_W` requires source, method, evidence, timestamp, and version.
- Equation 6: `v_I(p_i)` is produced from explicit request observations through versioned valuation rules.
- Equation 7: raw weighted sums are preserved, while the published illustration uses normalized weights.
- Equations 8 and 17: each binary descriptor has an explicit comparison function `s_i`.
- Equations 10-13: the policies reproduce `C_nav`, `C_hist`, `A_sailor`, `A_hist`, and both illustrative vectors.
- Equation 18: a threshold can only be applied to a normalized similarity score.
- Equation 23: audit events preserve every formal component needed to reproduce an evaluation.
- Section 7.3: unary and single-pair binary scoring remain linear in descriptor count under the article's comparator assumptions.

## Two implemented consumers

### Navigation Operations System

- selects `navigation-v1`;
- executes the policy associated with the sailor in `C_nav`;
- uses the same ship state and ontology;
- prioritizes structure and the disposition to navigate;
- demonstrates a joint requirement between descriptors.
- keeps that requirement in the versioned navigation policy.

### Heritage Preservation System

- selects `preservation-v1`;
- executes the policy associated with the historian in `C_hist`;
- uses the same ship state and ontology;
- prioritizes origin, historical value, and the monument role;
- receives different explanations and provenance.

The consumer process and the formal agent are deliberately distinct. A software system may execute a policy whose interpreting agent is a sailor, historian, institution, or another computational system.

## Deliberately unresolved matters

- universal weight elicitation;
- empirical validation of the vectors;
- automatic negotiation between policies;
- a theory of numerical identity;
- global transitivity of continuity;
- complete execution of the calculation in OWL.

These items are documented as limitations and are not presented as implemented capabilities.
