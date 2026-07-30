# Mapping Review Observations to Code

## Underspecified W(A,C)

**Change:** `WeightingPolicy` contains the agent, context, weights, notes, a non-empty `ProvenanceRecord`, and a versioned evaluation configuration. Policies are external and auditable files.

**Unresolved:** the project does not define a universal elicitation method. The method remains domain-dependent.

## Nature of context C

**Change:** `Context` represents the goal, time scope, environment, roles, and norms, corresponding to `C=<g,t,e,r,n>`. Empty components are rejected.

**Limitation:** this is not a complete context ontology.

The bundled policies reproduce `C_nav` and `C_hist` from Equations 10 and 11. Their formal agents are the sailor and historian from Equations 12 and 13; the HTTP consumers are the systems that execute those policies.

## Weights as psychological properties

**Change:** weights are treated as an explicit policy associated with an agent and context, not as an intrinsic property of either the entity or agent.

## Linear sum and dependencies

**Change:** an aggregation interface supports weighted average, weighted sum, and a rule-based strategy. Requirements and vetoes demonstrate non-independent combinations. `Agg_C` and its rules are part of the versioned contextual policy and cannot be replaced by a caller.

The raw weighted sum is preserved without clipping. Thresholded similarity requires a normalized score, preventing the magnitude of an unnormalized weight vector from changing an operational decision.

## Unary function versus binary relation

**Change:** endpoints, contracts, and responses are separate:

- `/v1/relevance` for `Rel_prag(I,A,C)`;
- `/v1/similarity` for `Sim_prag(I',I'',A,C)`.

## Identity, continuity, and transitivity

**Change:** the binary endpoint returns `operational_continuity_supported`, never `IdentityPreserved`. The response states that it makes no numerical-identity claim and warns about non-transitivity.

## OWL implementation

**Change:** RDF/OWL stores the stable structure with explicit descriptor subclasses for parts, structure, dispositions, provenance, qualities, and roles. It does not store observation defaults. Python evaluates explicit observations through policy-bound valuation functions.

## Instantiations and practical value

**Change:** two external systems consume the same API with traceable contributions and policies. Audit events contain the request, complete policy, and response. This demonstrates integration and operational explainability without claiming improved accuracy.

## Validation

**Partially addressed:** unit and software-integration tests verify the article's exact vectors, published illustrative scores, normalization constraint, policy provenance, descriptor anchoring, and API behavior.

**Not addressed:** there is no empirical evaluation of utility, performance, or weight quality. Such validation requires a domain and user study.

## Governance and negotiation

**Partially addressed:** policies are versioned, comparable, and auditable.

**Not addressed:** the project does not automatically reconcile conflicting policies; that decision remains institutional or governance-related.

## Computational considerations

**Change:** contribution sorting was removed so the unary and single-pair binary scoring kernels preserve the `O(n)` descriptor-count bound stated in Section 7.3, assuming constant-time descriptor comparisons.

**Limit:** string and collection comparators depend on input size. Batch candidate generation, indexing, and exhaustive pairwise resolution remain outside the API.
