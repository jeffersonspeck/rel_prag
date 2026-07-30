# Two Independent Systems Consuming the Same Foundation

## System 1: Navigation Operations System

File: `clients/navigation_system.py`

- policy: `navigation-v1`;
- goal: operational readiness;
- highest relevance: structure and disposition to float;
- uses a joint requirement between `p_structure` and `p_float`;
- consumes `POST /v1/relevance`.

## System 2: Heritage Preservation System

File: `clients/heritage_system.py`

- policy: `preservation-v1`;
- goal: historical preservation;
- highest relevance: origin, historical value, and monument role;
- consumes the same endpoint and entity state;
- receives policy-specific explanations and provenance.

## Why they are distinct systems

The consumers are separate processes with different goals, policies, and responsibilities. Integration occurs only over HTTP. They do not directly import internal engine classes and do not modify the RDF file.

This organization demonstrates that two applications can share the same ontology while retaining contextualized, auditable, and versioned policies.
