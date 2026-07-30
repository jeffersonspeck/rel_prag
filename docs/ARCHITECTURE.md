# Architecture and Design Decisions

## 1. Layer separation

The implementation has four layers:

1. **Stable ontology**: `data/theseus_ontology.ttl`, which implements `S(I)` from Equation 1 and the ship schema from Equation 9.
2. **Epistemic-pragmatic policies**: versioned JSON files in `data/policies/` containing `W(A,C)`, `Pi_W`, `v`, `s`, `Agg_C`, interaction rules, and the operational threshold from the general schema in Equation 23.
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

The ontology does not provide default observation values. This preserves the distinction in Equation 1 between the stable schema `S(I)` and the separately represented current valuation `v_I(p_i)`.

## 3. Valuation and comparison

For Equation 6, raw observations are converted into comparable `v_I(p_i)` values through a policy-bound valuation specification:

- `normalized`: accepts an observation already expressed on `[0,1]`;
- `numeric_range`: maps a declared numerical interval onto `[0,1]`;
- `categorical`: maps declared categories onto `[0,1]`.

Binary similarity implements Equations 8 and 17 with one explicit comparator `s_i` per descriptor. Comparator choices and ranges are stored in the same versioned policy as the weighting vector.

## 4. Aggregation

`Agg_C` is implemented as a replaceable strategy:

- `weighted_average`: a normalized, comparable result;
- `weighted_sum`: a direct implementation of the illustrative equation;
- `rule_aware`: support for synergy, redundancy, requirements, and vetoes.

The weighted sum preserves Equation 7 and is not treated as a universal definition of the model. Its raw result is not clipped. The normalization condition following Equation 7 is enforced before the threshold in Equation 18 can support an operational decision.

Aggregation strategies and interaction rules cannot be replaced by an API caller. They belong to the context-bound, versioned evaluation configuration.

## 5. Relevance and similarity

### Unary relevance

```text
Rel_prag(I,A,C)
```

Equation 6 evaluates an entity under a policy. It is used by the navigation and preservation systems.

### Binary similarity

```text
Sim_prag(I',I'',A,C)
```

Equation 8 compares two records or states. The result may support `ContextContinuitySupport` under Equation 18.

The API response always sets `numerical_identity_claimed=false` and includes an explicit non-transitivity warning.

## 6. Auditability

Each audit event stores:

- the complete observation or comparison request;
- the complete versioned policy;
- the resulting measure, contributions, warnings, and operational decision.

This record is sufficient to reconstruct the implemented components of Equation 23: `I`, `S(I)`, `A`, `C`, `W(A,C)`, `Pi_W`, `v`, `s`, and `Agg_C`.

## 7. Computational bounds

The scoring kernels preserve the descriptor-count bounds stated in Section 7.3:

- unary relevance is `O(n)`;
- single-pair similarity is `O(n)` when every `s_i` is constant-time;
- rule-aware aggregation adds work proportional to total rule arity.

No contribution sorting is performed. When comparator inputs have variable size, the more precise binary cost includes the cost of every `s_i`. Batch evaluation, candidate generation, indexing, and exhaustive `O(m^2 n)` entity resolution remain outside the single-pair API.

The complete equation-to-code map is available in `docs/FORMALIZATION_MAPPING.md`.
