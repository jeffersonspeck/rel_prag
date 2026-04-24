"""
decision_support_example.py

Exemplo 4: apoio à decisão.
Compara alternativas de ação sobre o Navio de Teseu segundo cada perfil.

Como executar:
    python decision_support_example.py
"""

from typing import Dict, Any, List
from common import get_profile, ELEMENTS, print_json


ALTERNATIVES = [
    {
        "id": "alt_001",
        "label": "Colocar o navio novamente em navegação",
        "impact": {
            "p_material": 0.3,
            "p_estrutura": 0.8,
            "p_flutuar": 1.0,
            "p_origem": 0.1,
            "p_valor_historico": 0.1,
            "p_papel_monumento": 0.0,
        },
    },
    {
        "id": "alt_002",
        "label": "Preservar o navio como monumento",
        "impact": {
            "p_material": 0.8,
            "p_estrutura": 0.5,
            "p_flutuar": 0.0,
            "p_origem": 1.0,
            "p_valor_historico": 1.0,
            "p_papel_monumento": 1.0,
        },
    },
    {
        "id": "alt_003",
        "label": "Restaurar parcialmente e manter exposição controlada",
        "impact": {
            "p_material": 0.7,
            "p_estrutura": 0.8,
            "p_flutuar": 0.4,
            "p_origem": 0.8,
            "p_valor_historico": 0.9,
            "p_papel_monumento": 0.8,
        },
    },
]


def evaluate_alternative(alternative: Dict[str, Any], profile_name: str) -> float:
    profile = get_profile(profile_name)
    weights = profile["weights"]

    score = 0.0
    for element in ELEMENTS:
        score += weights[element.id] * alternative["impact"].get(element.id, 0.0)

    return round(score, 4)


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
        "note": "O resultado organiza alternativas segundo o perfil interpretativo; não substitui validação por especialistas.",
    }


if __name__ == "__main__":
    print_json({
        "marinheiro": decision_support("marinheiro"),
        "historiador": decision_support("historiador"),
    })
