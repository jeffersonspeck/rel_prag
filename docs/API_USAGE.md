# API Usage

## Contextual relevance

```bash
curl -X POST http://127.0.0.1:8000/v1/relevance \
  -H "Content-Type: application/json" \
  -d '{
    "ontology_id": "theseus",
    "entity_id": "TheseusShip",
    "policy_id": "navigation-v1",
    "descriptor_values": {
      "p_material": 0.2,
      "p_structure": 1.0,
      "p_float": 1.0,
      "p_origin": 1.0,
      "p_historical_value": 0.8,
      "p_monument_role": 1.0
    },
    "aggregator": "weighted_average"
  }'
```

The response contains:

- the normalized result;
- the raw result;
- each descriptor's contribution;
- the agent and context;
- policy provenance;
- validity warnings.

## Contextual similarity

```bash
curl -X POST http://127.0.0.1:8000/v1/similarity \
  -H "Content-Type: application/json" \
  -d '{
    "ontology_id": "theseus",
    "entity_id": "TheseusShip",
    "policy_id": "preservation-v1",
    "left_record_id": "ship-t1",
    "right_record_id": "ship-t2",
    "left_values": {
      "p_material": 0.2,
      "p_structure": 1.0,
      "p_float": 1.0,
      "p_origin": 1.0,
      "p_historical_value": 0.8,
      "p_monument_role": 1.0
    },
    "right_values": {
      "p_material": 0.1,
      "p_structure": 0.95,
      "p_float": 0.9,
      "p_origin": 1.0,
      "p_historical_value": 0.85,
      "p_monument_role": 1.0
    },
    "threshold": 0.85
  }'
```

The `operational_continuity_supported` field is a contextual operational decision. The `numerical_identity_claimed` field always remains `false`.
