"""Example 4: decision support ranked by Rel_prag weights."""

from typing import Any, Dict, List

from common import ELEMENTS, get_profile, print_json

ALTERNATIVES = [
    {"id": "alt_001", "label": "Return the ship to navigation", "impact": {"p_material": 0.3, "p_estrutura": 0.8, "p_flutuar": 1.0, "p_origem": 0.1, "p_valor_historico": 0.1, "p_papel_monumento": 0.0}},
    {"id": "alt_002", "label": "Preserve the ship as a monument", "impact": {"p_material": 0.8, "p_estrutura": 0.5, "p_flutuar": 0.0, "p_origem": 1.0, "p_valor_historico": 1.0, "p_papel_monumento": 1.0}},
    {"id": "alt_003", "label": "Partially restore and keep controlled exhibition", "impact": {"p_material": 0.7, "p_estrutura": 0.8, "p_flutuar": 0.4, "p_origem": 0.8, "p_valor_historico": 0.9, "p_papel_monumento": 0.8}},
]


def evaluate_alternative(alternative: Dict[str, Any], profile_name: str) -> float:
    weights = get_profile(profile_name)["weights"]
    return round(sum(weights[element.id] * alternative["impact"].get(element.id, 0.0) for element in ELEMENTS), 4)


def decision_support(profile_name: str):
    profile = get_profile(profile_name)

    evaluated: List[Dict[str, Any]] = []
    for alternative in ALTERNATIVES:
        evaluated.append({
            "id": alternative["id"],
            "label": alternative["label"],
            "score": evaluate_alternative(alternative, profile_name),
            "impact": alternative["impact"],
        })

    evaluated.sort(key=lambda item: item["score"], reverse=True)

    return {
        "application": "decision_support",
        "agent": profile["agent"],
        "context": profile["context"],
        "interpretive_role": profile["interpretive_role"],
        "ranked_alternatives": evaluated,
        "note": "This ranking organizes alternatives by interpretive profile and does not replace expert validation.",
    }


if __name__ == "__main__":
    print_json({"sailor": decision_support("sailor"), "historian": decision_support("historian")})
