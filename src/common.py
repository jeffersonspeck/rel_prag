"""Módulo compartilhado para exemplos epistêmico-pragmáticos.

A ontologia (data/theseus_ontology.ttl) contém apenas a base estável S(I_navio).
Perfis interpretativos ficam no código de aplicação e sempre referenciam os
mesmos elementos carregados da ontologia.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from rdflib import Graph, Namespace, RDFS

from demo_relevance import calculate_relevance

BASE_DIR = Path(__file__).resolve().parents[1]
TTL_PATH = BASE_DIR / "data" / "theseus_ontology.ttl"
EX = Namespace("https://example.org/theseus#")


@dataclass(frozen=True)
class OntologicalElement:
    id: str
    label: str
    description: str
    ontological_value: float = 1.0


ENTITY = {
    "id": "theseus:ShipOfTheseus",
    "label": "Ship of Theseus",
    "type": "theseus:MaterialEntity",
    "description": "Material entity analyzed through ontologically grounded elements.",
}

PROFILE_DEFINITIONS = {
    "sailor": {
        "agent": {"id": "theseus:Sailor", "label": "Sailor"},
        "context": {"id": "theseus:NavigationContext", "label": "Navigation"},
        "interpretive_role": "Functional navigation object",
        "weights": {
            "p_material": 0.2,
            "p_estrutura": 0.8,
            "p_flutuar": 1.0,
            "p_origem": 0.1,
            "p_valor_historico": 0.1,
            "p_papel_monumento": 0.0,
        },
    },
    "historian": {
        "agent": {"id": "theseus:Historian", "label": "Historian"},
        "context": {"id": "theseus:HistoricalPreservationContext", "label": "Historical preservation"},
        "interpretive_role": "Historical and symbolic preservation object",
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


def _load_graph() -> Graph:
    if not TTL_PATH.exists():
        raise FileNotFoundError(f"TTL ontology not found at {TTL_PATH}. Run src/create_theseus_ontology.py first.")

    graph = Graph()
    graph.parse(TTL_PATH, format="turtle")
    return graph


def _build_elements(graph: Graph) -> List[OntologicalElement]:
    elements: List[OntologicalElement] = []
    for element in graph.objects(EX.TheseusShip, EX.hasElement):
        element_id = str(element).split("#")[-1]
        value = float(next(graph.objects(element, EX.elementValue), 1.0))
        label = str(next(graph.objects(element, RDFS.label), element_id))
        description = str(next(graph.objects(element, RDFS.comment), "Ontology element loaded from TTL."))
        elements.append(
            OntologicalElement(
                id=element_id,
                label=label,
                description=description,
                ontological_value=value,
            )
        )

    return sorted(elements, key=lambda e: e.id)


def _build_profiles() -> Dict[str, Dict[str, Any]]:
    element_ids = {element.id for element in ELEMENTS}
    profiles: Dict[str, Dict[str, Any]] = {}

    for profile_name, profile_data in PROFILE_DEFINITIONS.items():
        weights = profile_data["weights"]
        missing = element_ids - set(weights.keys())
        unknown = set(weights.keys()) - element_ids
        if missing or unknown:
            raise ValueError(
                f"Profile '{profile_name}' inconsistent with ontology elements. "
                f"Missing={sorted(missing)} Unknown={sorted(unknown)}"
            )

        profiles[profile_name] = {
            "agent": profile_data["agent"],
            "context": profile_data["context"],
            "interpretive_role": profile_data["interpretive_role"],
            "weights": weights,
        }

    return profiles


_GRAPH = _load_graph()
ELEMENTS: List[OntologicalElement] = _build_elements(_GRAPH)
PROFILES: Dict[str, Dict[str, Any]] = _build_profiles()


def get_profile(profile_name: str) -> Dict[str, Any]:
    try:
        return PROFILES[profile_name]
    except KeyError as exc:
        available = ", ".join(PROFILES.keys())
        raise ValueError(f"Invalid profile: {profile_name}. Use one of: {available}.") from exc


def calculate_ranking(profile_name: str) -> List[Dict[str, Any]]:
    profile = get_profile(profile_name)
    weights = profile["weights"]
    element_values = {element.id: element.ontological_value for element in ELEMENTS}
    total_relevance = float(calculate_relevance(element_values, weights))

    ranking = []
    for element in ELEMENTS:
        weight = weights.get(element.id, 0.0)
        relevance = weight * element.ontological_value
        ranking.append(
            {
                "element_id": element.id,
                "element": element.label,
                "description": element.description,
                "weight": round(weight, 4),
                "ontological_value": round(element.ontological_value, 4),
                "relevance": round(relevance, 4),
                "normalized_contribution": round((relevance / total_relevance) if total_relevance else 0.0, 4),
            }
        )

    return sorted(ranking, key=lambda item: item["relevance"], reverse=True)


def build_base_response(profile_name: str) -> Dict[str, Any]:
    profile = get_profile(profile_name)
    return {
        "entity": ENTITY,
        "agent": profile["agent"],
        "context": profile["context"],
        "interpretive_role": profile["interpretive_role"],
        "formula": "Rel_prag(I,A,C) = Σ(w_i(A,C) * v(p_i))",
        "ranking": calculate_ranking(profile_name),
    }


def run_simulation() -> Dict[str, Any]:
    """Executa a simulação dos perfis disponíveis usando a ontologia como base."""
    return {
        profile_name: build_base_response(profile_name)
        for profile_name in sorted(PROFILES.keys())
    }


def print_json(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
