"""
common.py

Módulo comum para os exemplos de uso da camada epistêmico-pragmática
baseada no exemplo do Navio de Teseu.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass(frozen=True)
class OntologicalElement:
    id: str
    label: str
    description: str
    ontological_value: float = 1.0


ENTITY = {
    "id": "theseus:ShipOfTheseus",
    "label": "Navio de Teseu",
    "type": "theseus:MaterialEntity",
    "description": "Entidade material analisada por elementos ontologicamente ancorados."
}


ELEMENTS: List[OntologicalElement] = [
    OntologicalElement("p_material", "Composição material", "Partes físicas e materialidade do navio."),
    OntologicalElement("p_estrutura", "Organização estrutural", "Forma, configuração e estabilidade estrutural."),
    OntologicalElement("p_flutuar", "Capacidade de flutuar", "Disposição funcional relacionada à navegação."),
    OntologicalElement("p_origem", "Origem", "Procedência e continuidade histórica."),
    OntologicalElement("p_valor_historico", "Valor histórico", "Importância simbólica, patrimonial ou documental."),
    OntologicalElement("p_papel_monumento", "Papel de monumento", "Papel contextual em práticas de preservação."),
]


PROFILES: Dict[str, Dict[str, Any]] = {
    "marinheiro": {
        "agent": {"id": "theseus:Sailor", "label": "Marinheiro"},
        "context": {"id": "theseus:NavigationContext", "label": "Navegação"},
        "interpretive_role": "Objeto funcional de navegação",
        "weights": {
            "p_material": 0.2,
            "p_estrutura": 0.8,
            "p_flutuar": 1.0,
            "p_origem": 0.1,
            "p_valor_historico": 0.1,
            "p_papel_monumento": 0.0,
        },
    },
    "historiador": {
        "agent": {"id": "theseus:Historian", "label": "Historiador"},
        "context": {"id": "theseus:HistoricalPreservationContext", "label": "Preservação histórica"},
        "interpretive_role": "Objeto de preservação histórica e simbólica",
        "weights": {
            "p_material": 0.9,
            "p_estrutura": 0.4,
            "p_flutuar": 0.1,
            "p_origem": 1.0,
            "p_valor_historico": 1.0,
            "p_papel_monumento": 0.9,
        },
    },
}


def get_profile(profile_name: str) -> Dict[str, Any]:
    try:
        return PROFILES[profile_name]
    except KeyError as exc:
        available = ", ".join(PROFILES.keys())
        raise ValueError(f"Perfil inválido: {profile_name}. Use um destes: {available}.") from exc


def calculate_relevance(profile_name: str) -> List[Dict[str, Any]]:
    profile = get_profile(profile_name)
    weights = profile["weights"]

    ranking = []
    for element in ELEMENTS:
        weight = weights[element.id]
        relevance = weight * element.ontological_value
        ranking.append({
            "element_id": element.id,
            "element": element.label,
            "description": element.description,
            "weight": weight,
            "ontological_value": element.ontological_value,
            "relevance": round(relevance, 4),
        })

    return sorted(ranking, key=lambda item: item["relevance"], reverse=True)


def build_base_response(profile_name: str) -> Dict[str, Any]:
    profile = get_profile(profile_name)
    return {
        "entity": ENTITY,
        "agent": profile["agent"],
        "context": profile["context"],
        "interpretive_role": profile["interpretive_role"],
        "ranking": calculate_relevance(profile_name),
    }


def print_json(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
