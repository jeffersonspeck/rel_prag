def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_relevance_endpoint(client):
    response = client.post(
        "/v1/relevance",
        json={
            "policy_id": "navigation-v1",
            "descriptor_values": {
                "p_material": 0.2,
                "p_structure": 1.0,
                "p_float": 1.0,
                "p_origin": 1.0,
                "p_historical_value": 0.8,
                "p_monument_role": 1.0
            }
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["policy_id"] == "navigation-v1"
    assert payload["provenance"]["version"] == "1.0.0"
