"""Independent consumer 1: navigation operations system."""

from __future__ import annotations

import argparse
import json

import httpx

SHIP_STATE = {
    "p_material": 0.2,
    "p_structure": 1.0,
    "p_float": 1.0,
    "p_origin": 1.0,
    "p_historical_value": 0.8,
    "p_monument_role": 1.0
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    payload = {
        "ontology_id": "theseus",
        "entity_id": "TheseusShip",
        "policy_id": "navigation-v1",
        "descriptor_values": SHIP_STATE,
        "aggregator": "rule_aware",
        "interaction_rules": [
            {
                "rule_id": "navigation-capability-requirement",
                "kind": "requirement",
                "descriptors": ["p_structure", "p_float"],
                "trigger": 0.7,
                "coefficient": 0.0,
                "description": "Operational navigation requires both adequate structure and floating disposition."
            }
        ]
    }

    response = httpx.post(f"{args.base_url}/v1/relevance", json=payload, timeout=10.0)
    response.raise_for_status()
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
