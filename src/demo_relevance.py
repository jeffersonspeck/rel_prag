"""Demonstration of the pragmatic relevance formula based on the ontology.

The ontology provides the ontological elements and values v(p_i).
Weights w_i(A,C) are defined in application profiles.

Formula:
    Rel_prag(I,A,C) = Σ(w_i(A,C) * v(p_i))
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Dict

from rdflib import Graph, Namespace

BASE_DIR = Path(__file__).resolve().parents[1]
TTL_PATH = BASE_DIR / "data" / "theseus_ontology.ttl"
EX = Namespace("https://example.org/theseus#")

SIMULATION_WEIGHTS: Dict[str, Dict[str, Decimal]] = {
    "sailor": {
        "p_material": Decimal("0.2"),
        "p_estrutura": Decimal("0.8"),
        "p_flutuar": Decimal("1.0"),
        "p_origem": Decimal("0.1"),
        "p_valor_historico": Decimal("0.1"),
        "p_papel_monumento": Decimal("0.0"),
    },
    "historian": {
        "p_material": Decimal("0.9"),
        "p_estrutura": Decimal("0.4"),
        "p_flutuar": Decimal("0.1"),
        "p_origem": Decimal("1.0"),
        "p_valor_historico": Decimal("1.0"),
        "p_papel_monumento": Decimal("0.9"),
    },
}


def decimal_from_literal(value) -> Decimal:
    return Decimal(str(value))


def get_element_values(graph: Graph) -> Dict[str, Decimal]:
    values: Dict[str, Decimal] = {}

    for element in graph.objects(EX.TheseusShip, EX.hasElement):
        literal_value = next(graph.objects(element, EX.elementValue), None)
        if literal_value is None:
            continue
        values[str(element).split("#")[-1]] = decimal_from_literal(literal_value)

    return values


def calculate_relevance(element_values: Dict[str, float | Decimal], weights: Dict[str, float | Decimal]) -> Decimal:
    relevance = Decimal("0")

    for element_name, element_value in element_values.items():
        weight = weights.get(element_name, Decimal("0"))
        relevance += decimal_from_literal(weight) * decimal_from_literal(element_value)

    return relevance


def simulate_profiles(graph: Graph) -> Dict[str, Decimal]:
    element_values = get_element_values(graph)
    return {
        profile_name: calculate_relevance(element_values, weights)
        for profile_name, weights in SIMULATION_WEIGHTS.items()
    }


def main() -> None:
    if not TTL_PATH.exists():
        raise FileNotFoundError(f"TTL file not found: {TTL_PATH}. Run create_theseus_ontology.py first.")

    graph = Graph()
    graph.parse(TTL_PATH, format="turtle")

    element_values = get_element_values(graph)
    print("Elements loaded from the base ontology S(I_ship):")
    for element_name, value in sorted(element_values.items()):
        print(f"- {element_name}: v(p_i)={value}")

    print("\nProfile simulation (weights external to ontology):")
    for profile_name, rel in simulate_profiles(graph).items():
        print(f"- {profile_name}: Rel_prag={rel}")


if __name__ == "__main__":
    main()
