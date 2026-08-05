# Changelog

All notable changes are documented here. Formal references follow the article **The Ship of Theseus Paradox and Epistemic-Pragmatic Weighting in Ontological Modeling**.

## [Unreleased]

- Realigned all section and equation references with the supplied 14-page final PDF (Equations 1-14).
- Added article/software citation metadata, BibTeX, and an explicit rights notice.
- Added the canonical article-to-code traceability and completeness audit.
- Added an automated reproduction of the Equation 12-13 geographic example.
- Removed an obsolete caller-supplied `aggregator` field from the heritage HTTP client and added a client-contract regression test.

## [1.1.0] - 2026-07-30

### Formalization alignment

| Article reference | Implementation change | Verification |
| --- | --- | --- |
| Section 3.1 and Equation 1, `C=<g,t,e,r_A,n>` | Context fields, roles, and norms must contain meaningful values. Empty contexts are rejected. | `test_context_and_provenance_cannot_be_empty` |
| Equation 2, `S(I)={p_1,...,p_n}` | The stable ontology contains only the admissible descriptor schema. Observation defaults were removed from RDF/OWL. | `test_stable_ontology_contains_descriptors_but_no_weights` |
| Equation 2, typed and ontologically anchored `p_i` | The six Ship of Theseus descriptors now use explicit OWL subclasses for parts, structure, dispositions, provenance, qualities, and roles. | `test_stable_ontology_contains_descriptors_but_no_weights` |
| Equation 4, `W(A,C)` and `w_i in [0,1]` | Policies enforce unit-interval weights, reject all-zero vectors, and must cover the complete descriptor schema. | `test_each_policy_has_provenance_and_matches_ontology` |
| Equation 5, `Pi_W=<source,method,evidence,timestamp,version>` | Provenance fields and supporting evidence are mandatory and cannot be blank. | `test_context_and_provenance_cannot_be_empty` |
| Equations 3 and 6, `v_I(p_i)` and `Rel_prag` | Relevance requests must provide a complete observation record. Versioned valuation rules convert normalized, ranged, or categorical observations into comparable descriptor values. | `test_relevance_requires_an_explicit_complete_observation`, `test_domain_valuations_convert_raw_observations_explicitly` |
| Equation 7, linear weighted sum | The raw linear result is no longer clipped. The response states whether the resulting scale is normalized and comparable. | `test_linear_weighted_sum_preserves_the_equation_without_clipping` |
| Equation 8, descriptor-specific `s_i` | Every policy must define one comparison function for every descriptor. Comparator definitions are returned with similarity contributions. | `test_each_policy_has_provenance_and_matches_ontology`, `test_binary_similarity_is_not_numerical_identity` |
| Discussion after Equation 8 and Equation 13, thresholded similarity | Operational continuity can only use normalized scores. An unnormalized weighted sum is rejected before threshold evaluation. | `test_thresholded_weighted_sum_requires_normalized_weights` |
| Sections 3-4, complete evaluation architecture | Valuations, comparators, relevance aggregation, similarity aggregation, interaction rules, and threshold are versioned with the policy instead of being supplied ad hoc by callers. | `test_callers_cannot_replace_the_context_bound_aggregator` |
| Sections 4.1-4.2, traceability | Audit events preserve the complete request, policy configuration, and response needed to reproduce a contextual decision. | `test_audit_record_preserves_request_policy_and_response` |
| Equations 9-11, Ship schema and illustrative vectors | Policies reproduce the sailor and historian agents, both weight vectors, and the published scores of approximately `0.92` and `0.79`; context tuple contents are explicit implementation choices. | `test_policies_use_the_exact_weight_vectors_from_the_article`, `test_two_systems_consume_same_entity_with_distinct_policies` |
| Implementation complexity analysis | Contribution sorting was removed so the unary and single-pair binary kernels remain linear in descriptor count under constant-time comparator assumptions. The article itself makes no runtime-complexity claim. | Formal-order contribution assertions |

### API changes

- Removed caller-provided `aggregator` and `interaction_rules` from relevance requests.
- Removed caller-provided `aggregator`, `interaction_rules`, `comparators`, and `threshold` from similarity requests.
- Made relevance observation values mandatory and complete.
- Added `evaluation_version` and `score_is_normalized` to responses.
- Added the applied comparator specification to every similarity contribution.

These are intentional breaking changes. The selected policy now determines the complete contextual evaluation procedure.

### Audit changes

- Audit payloads now contain `request`, `policy`, and `response`.
- The stored policy includes `W(A,C)`, `Pi_W`, valuation functions, comparison functions, aggregation operators, interaction rules, and the operational threshold.

## [1.0.0] - 2026-07-30

### Initial platform

- Introduced the stable Ship of Theseus ontology.
- Moved weighting vectors into external versioned policies.
- Added unary relevance and binary similarity endpoints.
- Added independent navigation and heritage-preservation consumers.
- Added provenance, explanations, audit output, and automated tests.
