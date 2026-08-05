"""Independent consumer 2: heritage preservation system."""

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
        "policy_id": "preservation-v1",
        # The system executes the historian policy from Equation 11.
        # Agg_C remains versioned with that policy and is not caller-supplied.
        "descriptor_values": SHIP_STATE,
    }

    response = httpx.post(f"{args.base_url}/v1/relevance", json=payload, timeout=10.0)
    response.raise_for_status()
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
