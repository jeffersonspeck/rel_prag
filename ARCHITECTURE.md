# Architecture and Design Decisions

## 1. Layer separation

The implementation has four layers:

1. **Stable ontology**: `data/theseus_ontology.ttl`, which contains the entity and its allowed descriptors.
2. **Epistemic-pragmatic policies**: versioned JSON files in `data/policies/`.
3. **Computational engine**: the `src/epm` package, responsible for validation, aggregation, comparison, and explanation.
4. **Integration**: the FastAPI API and external consumers in `clients/`.

Weights, agents, contexts, and decisions are not stored as intrinsic properties of the ship. They remain in external policies and are associated with provenance records.

## 2. Ontology and OWL

RDF/OWL is used to:

- identify the entity;
- declare the stable descriptor schema;
- type and document descriptors;
- validate which properties a policy may weight.

The Python engine is used to:

- calculate relevance and similarity;
- apply aggregators and rules;
- evaluate thresholds;
- produce explanations and audit records.

This separation addresses the practical limitation of performing numerical calculations and contextual policy evaluation exclusively within the OWL and reasoner ecosystem.

## 3. Aggregation

`Agg_C` is implemented as a replaceable strategy:

- `weighted_average`: a normalized, comparable result;
- `weighted_sum`: a direct implementation of the illustrative equation;
- `rule_aware`: support for synergy, redundancy, requirements, and vetoes.

The weighted sum is not treated as a universal definition of the model.

## 4. Relevance and similarity

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
