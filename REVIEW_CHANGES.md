# Mapping Review Observations to Code

## Underspecified W(A,C)

**Change:** `WeightingPolicy` contains the agent, context, weights, notes, and a `ProvenanceRecord`. Policies are external, versioned, and auditable files.

**Unresolved:** the project does not define a universal elicitation method. The method remains domain-dependent.

## Nature of context C

**Change:** `Context` represents the goal, time scope, environment, roles, and norms, corresponding to `C=<g,t,e,r,n>`.

**Limitation:** this is not a complete context ontology.

## Weights as psychological properties

**Change:** weights are treated as an explicit policy associated with an agent and context, not as an intrinsic property of either the entity or agent.

## Linear sum and dependencies

**Change:** an aggregation interface now supports weighted average, weighted sum, and a rule-based strategy. Requirements and vetoes demonstrate non-independent combinations.

## Unary function versus binary relation

**Change:** endpoints, contracts, and responses are separate:

- `/v1/relevance` for `Rel_prag(I,A,C)`;
- `/v1/similarity` for `Sim_prag(I',I'',A,C)`.

## Identity, continuity, and transitivity

**Change:** the binary endpoint returns `operational_continuity_supported`, never `IdentityPreserved`. The response states that it makes no numerical-identity claim and warns about non-transitivity.

## OWL implementation

**Change:** RDF/OWL stores the stable structure. Python performs the calculations and evaluates policies. This separation is documented and tested.

## Instantiations and practical value

**Change:** two external systems consume the same API with traceable contributions and policies. This demonstrates integration and operational explainability without claiming improved accuracy.

## Validation

**Partially addressed:** unit and software-integration tests are available.

**Not addressed:** there is no empirical evaluation of utility, performance, or weight quality. Such validation requires a domain and user study.

## Governance and negotiation

**Partially addressed:** policies are versioned, comparable, and auditable.

**Not addressed:** the project does not automatically reconcile conflicting policies; that decision remains institutional or governance-related.
