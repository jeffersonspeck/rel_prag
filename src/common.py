"""
common.py

Shared module for epistemic-pragmatic examples based on the Ship of Theseus ontology.
All element structures and profile weights are loaded from data/theseus_ontology.ttl.
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

ENGLISH_ELEMENT_LABELS = {
    "p_material": ("Material composition", "Physical parts and material substrate of the ship."),
    "p_estrutura": ("Structural organization", "Configuration, form, and structural stability."),
    "p_flutuar": ("Floating and navigation disposition", "Realizable capability related to floating and navigation."),
    "p_origem": ("Origin and provenance", "Origin, provenance, and historical continuity."),
    "p_valor_historico": ("Historical value", "Historical, symbolic, and memorial relevance."),
    "p_papel_monumento": ("Monument role", "Contextual role in historical preservation practices."),
}

PROFILE_METADATA = {
    "W_Marinheiro_Navegacao": {
        "name": "sailor",
        "agent": {"id": "theseus:Sailor", "label": "Sailor"},
        "context": {"id": "theseus:NavigationContext", "label": "Navigation"},
        "interpretive_role": "Functional navigation object",
    },
    "W_Historiador_Preservacao": {
        "name": "historian",
        "agent": {"id": "theseus:Historian", "label": "Historian"},
        "context": {"id": "theseus:HistoricalPreservationContext", "label": "Historical preservation"},
        "interpretive_role": "Historical and symbolic preservation object",
    },
}


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


def _load_graph() -> Graph:
    if not TTL_PATH.exists():
        raise FileNotFoundError(f"TTL ontology not found at {TTL_PATH}. Run src/create_theseus_ontology.py first.")

    graph = Graph()
    graph.parse(TTL_PATH, format="turtle")
    return graph


def _build_elements(graph: Graph) -> List[OntologicalElement]:
    elements: List[OntologicalElement] = []
    for element in graph.objects(EX.TheseusShip, EX.hasElement):
        element_id = element.split("#")[-1]
        value = next(graph.objects(element, EX.elementValue), 1.0)
        label, description = ENGLISH_ELEMENT_LABELS.get(
            element_id,
            (element_id.replace("_", " ").title(), "Ontology element loaded from TTL."),
        )
        elements.append(
            OntologicalElement(
                id=element_id,
                label=label,
                description=description,
                ontological_value=float(value),
            )
        )

    return sorted(elements, key=lambda e: e.id)


def _extract_weights(graph: Graph, vector_name: str) -> Dict[str, float]:
    weights: Dict[str, float] = {}
    vector = EX[vector_name]
    for assignment in graph.objects(vector, EX.hasWeightAssignment):
        element = next(graph.objects(assignment, EX.forElement), None)
        weight = next(graph.objects(assignment, EX.weightValue), None)
        if element is None or weight is None:
            continue
        element_name = element.split("#")[-1]
        weights[element_name] = float(weight)
    return weights


def _build_profiles(graph: Graph) -> Dict[str, Dict[str, Any]]:
    profiles: Dict[str, Dict[str, Any]] = {}
    for vector_name, metadata in PROFILE_METADATA.items():
        profiles[metadata["name"]] = {
            "agent": metadata["agent"],
            "context": metadata["context"],
            "interpretive_role": metadata["interpretive_role"],
            "weights": _extract_weights(graph, vector_name),
        }
    return profiles


_GRAPH = _load_graph()
ELEMENTS: List[OntologicalElement] = _build_elements(_GRAPH)
PROFILES: Dict[str, Dict[str, Any]] = _build_profiles(_GRAPH)


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
        "ranking": calculate_ranking(profile_name),
    }


def print_json(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
