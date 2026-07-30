# Architecture and Design Decisions

## 1. Layer separation

The implementation has four layers:

1. **Stable ontology**: `data/theseus_ontology.ttl`, which contains the entity and its typed, admissible descriptor schema `S(I)`.
2. **Epistemic-pragmatic policies**: versioned JSON files in `data/policies/` containing `W(A,C)`, `Pi_W`, `v`, `s`, `Agg_C`, interaction rules, and the operational threshold.
3. **Computational engine**: the `src/epm` package, responsible for validation, aggregation, comparison, and explanation.
4. **Integration**: the FastAPI API and external consumers in `clients/`.

Weights, agents, contexts, observations, and decisions are not stored as intrinsic properties of the ship. Observed values are supplied with each request, while interpretation and evaluation settings remain in external policies with provenance and configuration versions.

## 2. Ontology and OWL

RDF/OWL is used to:

- identify the entity;
- declare the stable descriptor schema;
- type each descriptor as a part, structural aspect, disposition, provenance aspect, quality, or role;
- validate which properties a policy may weight.

The Python engine is used to:

- calculate relevance and similarity;
- apply aggregators and rules;
- evaluate thresholds;
- produce explanations and audit records.

This separation addresses the practical limitation of performing numerical calculations and contextual policy evaluation exclusively within the OWL and reasoner ecosystem.

The ontology does not provide default observation values. This preserves the distinction between the stable schema `S(I)` and the current valuation `v_I(p_i)`.

## 3. Valuation and comparison

Raw observations are converted into comparable values through a policy-bound valuation specification:

- `normalized`: accepts an observation already expressed on `[0,1]`;
- `numeric_range`: maps a declared numerical interval onto `[0,1]`;
- `categorical`: maps declared categories onto `[0,1]`.

Binary similarity uses one explicit comparator `s_i` per descriptor. Comparator choices and ranges are stored in the same versioned policy as the weighting vector.

## 4. Aggregation

`Agg_C` is implemented as a replaceable strategy:

- `weighted_average`: a normalized, comparable result;
- `weighted_sum`: a direct implementation of the illustrative equation;
- `rule_aware`: support for synergy, redundancy, requirements, and vetoes.

The weighted sum is not treated as a universal definition of the model. Its raw result is preserved without clipping. A thresholded operational decision rejects a weighted sum unless the policy weights already sum to one.

Aggregation strategies and interaction rules cannot be replaced by an API caller. They belong to the context-bound, versioned evaluation configuration.

## 5. Relevance and similarity

### Unary relevance

```text
Rel_prag(I,A,C)
```

Evaluates an entity under a policy. It is used by the navigation and preservation systems.

### Binary similarity

```text
Sim_prag(I',I'',A,C)
```

Compares two records or states. The result may support an operational-continuity decision.

The API response always sets `numerical_identity_claimed=false` and includes an explicit non-transitivity warning.

## 6. Auditability

Each audit event stores:

- the complete observation or comparison request;
- the complete versioned policy;
- the resulting measure, contributions, warnings, and operational decision.

This record is sufficient to reconstruct the applied `W(A,C)`, `Pi_W`, `v`, `s`, `Agg_C`, interaction rules, and threshold.
