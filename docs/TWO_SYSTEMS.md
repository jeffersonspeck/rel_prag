# Two Independent Systems Consuming the Same Foundation

## System 1: Navigation Operations System

File: `clients/navigation_system.py`

- policy: `navigation-v1`;
- formal agent: sailor;
- structured context: an explicit implementation of `C_nav` (Equation 1 supplies the context structure; Equation 10 supplies the sailor vector);
- goal: safe navigation;
- highest relevance: structure and disposition to float;
- uses a joint requirement between `p_structure` and `p_float`;
- obtains its valuation and aggregation procedure from the versioned policy;
- consumes `POST /v1/relevance`.

## System 2: Heritage Preservation System

File: `clients/heritage_system.py`

- policy: `preservation-v1`;
- formal agent: historian;
- structured context: an explicit implementation of `C_hist` (Equation 1 supplies the context structure; Equation 11 supplies the historian vector);
- goal: historical preservation;
- highest relevance: origin, historical value, and monument role;
- consumes the same endpoint and entity state;
- obtains its valuation and aggregation procedure from a different versioned policy;
- receives policy-specific explanations and provenance.

## Why they are distinct systems

The consumers are separate processes with different goals, policies, and responsibilities. Integration occurs only over HTTP. They do not directly import internal engine classes and do not modify the RDF file.

A consumer is not necessarily the formal agent `A`. In this implementation, each external system executes a policy associated with the human agent used in the article's illustration. This preserves the Equation 10-11 Ship profiles without conflating an integration process with the standpoint represented by its policy.

This organization demonstrates that two applications can share the same ontology while retaining contextualized, auditable, and versioned policies.
