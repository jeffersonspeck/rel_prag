# Uso da API

## Relevância contextual

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

A resposta contém:

- resultado normalizado;
- resultado bruto;
- contribuição por descritor;
- agente e contexto;
- proveniência da política;
- alertas de validade.

## Similaridade contextual

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

O campo `operational_continuity_supported` é uma decisão operacional contextual. O campo `numerical_identity_claimed` permanece sempre `false`.
