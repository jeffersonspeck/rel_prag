# Formalization-to-Code Mapping

This document maps the final PDF of **The Ship of Theseus Paradox and Epistemic-Pragmatic Weighting in Ontological Modeling** to the executable implementation. The PDF dated July 30, 2026 is the normative source for equation numbers and conceptual boundaries.

## Scope

The article presents a propositional formalization rather than a complete axiomatic system. The repository implements the Ship of Theseus instantiation and the reusable unary and binary evaluation operators. The geographic and educational sections demonstrate cross-domain use; their domain ontologies and datasets are not included here.

## Formal components

| Article | Formal meaning | Implementation |
| --- | --- | --- |
| Equation 1 | `S(I)={p_1,p_2,...,p_n}` is the finite schema of typed, ontologically anchored descriptors. | `data/theseus_ontology.ttl`, `scripts/create_theseus_ontology.py`, and `OntologyRepository`. |
| Equation 2 | `W(A,C)=[w_1(A,C),...,w_n(A,C)]`. | The `weights` field in each JSON policy and `WeightingPolicy`. |
| Equation 3 | `W(A,C)=W(A,<g,t,e,r,n>)`; every weight is conditioned by the structured context. | `Context` is stored with the vector in one immutable policy artifact. A context change requires a different policy or policy version. |
| Equation 4 | `w_i(A,C) in [0,1]`. | `UnitFloat` validates every weight; all-zero vectors are rejected because normalized aggregation would be undefined. |
| Equation 5 | `Pi_W=<source,method,evidence,timestamp,version>`. | `ProvenanceRecord` requires every component and rejects blank provenance. |
| Equation 6 | `Rel_prag(I,A,C)=Agg_C({(w_i(A,C),v_I(p_i))}_{i=1}^n)`. | `EpistemicPragmaticEngine.relevance`, policy-bound valuations, and aggregation strategies. |
| Equation 7 | `Rel_prag^lin=sum_i w_i(A,C)*v_I(p_i)`. | `weighted_sum` preserves the raw equation. `weighted_average` evaluates the same expression with normalized weights. `rule_aware` is used when the separability assumptions do not hold. |
| Equation 8 | `Sim_prag(I',I'',A,C)=Agg_C({(w_i(A,C),s_i(v_I'(p_i),v_I''(p_i)))}_{i=1}^n)`. | `EpistemicPragmaticEngine.similarity` and one policy-bound `ComparatorSpec` per descriptor. |
| Equation 9 | The ship schema contains material, structure, floating disposition, origin, historical value, and monument role. | The six typed descriptor individuals attached to `epm:TheseusShip`. |
| Equation 10 | `C_nav` is safe navigation, the current operational episode, maritime operation, sailor/operator roles, and seaworthiness/safety norms. | `data/policies/navigation-v1.json`. |
| Equation 11 | `C_hist` is historical preservation, a long-term horizon, a heritage setting, historian/curator roles, and authenticity/conservation norms. | `data/policies/preservation-v1.json`. |
| Equation 12 | `W(A_sailor,C_nav)≈[0.2,0.8,1.0,0.1,0.1,0.0]`. | `navigation-v1`; the normalized illustration produces `0.918182`, approximately `0.92`. |
| Equation 13 | `W(A_hist,C_hist)≈[0.9,0.4,0.1,1.0,1.0,0.9]`. | `preservation-v1`; the normalized illustration produces `0.786047`, approximately `0.79`. |
| Equations 14-17 | Territorial-unit descriptors, an expert policy, structured `C_TSN`, and weighted descriptor-specific similarity. | Supported by the generic schema, valuation, comparison, and aggregation contracts. No territorial ontology or batch entity-resolution dataset is bundled. |
| Equation 18 | `Sim_prag>=beta => ContextContinuitySupport(...)`. | `operational_continuity_supported`; threshold evaluation is rejected unless the score is normalized. `numerical_identity_claimed` is always `false`. |
| Equations 19-22 | Educational descriptors, contextual evidence weighting, and unary profile construction. | Supported by normalized, ranged, and categorical valuation specifications. No educational ontology or recommendation dataset is bundled. |
| Equation 23 | `<I,S(I),A,C,W(A,C),Pi_W,v,s,Agg_C>` is the general schema. | The request identifies `I` and observations; the ontology supplies `S(I)`; the selected policy supplies `A`, `C`, `W`, `Pi_W`, `v`, `s`, and `Agg_C`; the audit event preserves the complete execution. |

## Equation 6: unary relevance

The relevance path performs the following operations:

1. validate that the observation record covers exactly `S(I)`;
2. apply the policy's valuation function to obtain every `v_I(p_i)`;
3. pair each value with `w_i(A,C)`;
4. execute the policy's `Agg_C`;
5. return the score, raw score, normalization status, and per-descriptor contributions.

The API caller supplies observations, not mathematical policy. This prevents the same declared `A`, `C`, and `W(A,C)` from being combined with an unversioned aggregation rule.

## Equations 8 and 18: similarity and continuity support

The similarity path requires two complete records over the same `S(I)`. Each descriptor uses its declared comparison function `s_i`. The resulting score may support operational continuity only when it is normalized.

The response deliberately separates:

- `score`: contextual binary similarity;
- `threshold`: the policy's `beta`;
- `operational_continuity_supported`: the executable counterpart of `ContextContinuitySupport`;
- `numerical_identity_claimed`: always `false`.

The warning about non-transitivity follows the discussion after Equation 18. Longitudinal identity management still requires lineage, provenance, or global continuity constraints.

## Context and agent interpretation

The external consumer process is not automatically the formal agent `A`. The Navigation Operations System executes the policy associated with the sailor in `C_nav`; the Heritage Preservation System executes the policy associated with the historian in `C_hist`. This distinction keeps the systems as integration clients while preserving the article's illustrative agents and contexts.

## Computational complexity

The article states that the linear unary and single-pair binary operations are `O(n)` when descriptor access and each `s_i` are constant-time.

The implementation preserves that bound with respect to descriptor count:

- relevance valuation, weighting, aggregation, and contribution construction are linear in `n`;
- single-pair similarity is linear in `n` under the article's constant-time-comparator assumption;
- interaction-aware aggregation adds work proportional to the total number of descriptor references in its rules;
- contributions remain in formal descriptor order and are not sorted.

For comparators whose input size is not constant, the more precise similarity cost is:

```text
O(n + sum_i T(s_i) + total_rule_arity)
```

For example, string and set comparisons depend on string or collection size. The API evaluates one pair at a time. Candidate generation, indexing, `O(mn)` batch evaluation, and `O(m^2 n)` exhaustive entity resolution remain application-level concerns, as stated in Section 7.3.

## Traceability

Every JSONL audit event stores:

- the request and observation records;
- the complete versioned policy;
- the response and contributions.

Together these preserve every implemented component of Equation 23 and allow a result to be reproduced without relying on hidden caller settings.

## Analytical adequacy criteria

Section 3 evaluates the model through five analytical criteria. The implementation addresses them as follows:

1. **Conceptual coherence:** separate models represent the entity schema, agent, context, weighting policy, provenance, valuation, comparison, aggregation, and task-specific output.
2. **Construct separability:** RDF/OWL contains the stable reference layer; JSON policies contain the epistemic-pragmatic layer; requests contain current observations; responses contain task outputs.
3. **Policy traceability:** versioned policy files and complete audit events expose every setting that affects a result.
4. **Cross-domain applicability:** heterogeneous OWL descriptor types, multiple valuation modes, descriptor-specific comparators, and replaceable aggregators implement the general extension points.
5. **Explicit failure conditions:** the service rejects missing or unknown descriptors, blank context or provenance, non-comparable values, inconsistent policy schemas, unknown rule descriptors, and unnormalized threshold scores.

Passing these checks establishes internal and analytical consistency. It does not constitute empirical validation, predictive accuracy, or domain-level effectiveness.

## Article boundary conditions

The implementation does not claim:

- a universal procedure for eliciting or validating weights;
- empirical validity for the illustrative vectors;
- a complete ontology of context;
- automatic reconciliation of incompatible policies;
- numerical identity from similarity;
- transitive pairwise continuity;
- complete numerical inference in OWL;
- empirical runtime or scalability validation.

These are boundaries stated by the article, not missing advertised capabilities.

## Editorial ambiguity in Equation 20

In the final PDF, the paragraph introducing the educational weighting vector points to an unresolved equation reference, while Equation 20 repeats the historical-preservation context tuple. The repository does not invent a missing educational vector. It implements the general unary schema from Equations 6, 22, and 23 and leaves domain-specific educational weights to a future validated policy.
