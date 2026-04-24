"""Example 2: recommendation system with Rel_prag-based ranking."""

from typing import Any, Dict, List

from common import ELEMENTS, get_profile, print_json

ITEMS = [
    {
        "id": "item_001",
        "label": "Navigation readiness inspection",
        "attributes": {"p_material": 0.3, "p_estrutura": 0.9, "p_flutuar": 1.0, "p_origem": 0.1, "p_valor_historico": 0.1, "p_papel_monumento": 0.0},
    },
    {
        "id": "item_002",
        "label": "Historical authenticity report",
        "attributes": {"p_material": 0.8, "p_estrutura": 0.4, "p_flutuar": 0.1, "p_origem": 1.0, "p_valor_historico": 1.0, "p_papel_monumento": 0.7},
    },
    {
        "id": "item_003",
        "label": "Museum exhibition project",
        "attributes": {"p_material": 0.5, "p_estrutura": 0.3, "p_flutuar": 0.0, "p_origem": 0.8, "p_valor_historico": 1.0, "p_papel_monumento": 1.0},
    },
    {
        "id": "item_004",
        "label": "Structural repair plan",
        "attributes": {"p_material": 0.7, "p_estrutura": 1.0, "p_flutuar": 0.8, "p_origem": 0.2, "p_valor_historico": 0.2, "p_papel_monumento": 0.1},
    },
]


def score_item(item: Dict[str, Any], profile_name: str) -> float:
    weights = get_profile(profile_name)["weights"]
    return round(sum(weights[e.id] * item["attributes"].get(e.id, 0.0) for e in ELEMENTS), 4)


def recommend(profile_name: str) -> Dict[str, Any]:
    profile = get_profile(profile_name)
    ranked_items: List[Dict[str, Any]] = []
    for item in ITEMS:
        ranked_items.append({"id": item["id"], "label": item["label"], "score": score_item(item, profile_name), "attributes": item["attributes"]})

    ranked_items.sort(key=lambda item: item["score"], reverse=True)

    return {
        "application": "recommendation",
        "agent": profile["agent"],
        "context": profile["context"],
        "interpretive_role": profile["interpretive_role"],
        "recommendations": ranked_items,
    }


if __name__ == "__main__":
    print_json({"sailor": recommend("sailor"), "historian": recommend("historian")})
