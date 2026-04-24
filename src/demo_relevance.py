"""
Demonstrates pragmatic relevance calculation from the TTL ontology.

Implemented formula:

    Rel_prag(I,A,C) = sum(w_i(A,C) * v(p_i))
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Dict, Tuple

from rdflib import Graph, Namespace, RDFS

BASE_DIR = Path(__file__).resolve().parents[1]
TTL_PATH = BASE_DIR / "data" / "theseus_ontology.ttl"
EX = Namespace("https://example.org/theseus#")


def decimal_from_literal(value) -> Decimal:
    return Decimal(str(value))


def get_element_values(graph: Graph) -> Dict[str, Decimal]:
    values: Dict[str, Decimal] = {}

    for element in graph.objects(EX.TheseusShip, EX.hasElement):
        label = next(graph.objects(element, EX.elementValue), None)
        if label is None:
            continue
        values[element.split("#")[-1]] = decimal_from_literal(label)

    return values


def get_vector_weights(graph: Graph, vector_name: str) -> Tuple[str, Dict[str, Decimal]]:
    vector = EX[vector_name]
    label = next(graph.objects(vector, RDFS.label), None)

    weights: Dict[str, Decimal] = {}
    for assignment in graph.objects(vector, EX.hasWeightAssignment):
        element = next(graph.objects(assignment, EX.forElement), None)
        weight = next(graph.objects(assignment, EX.weightValue), None)

        if element is None or weight is None:
            continue

        element_name = element.split("#")[-1]
        weights[element_name] = decimal_from_literal(weight)

    return str(label or vector_name), weights


def calculate_relevance(element_values: Dict[str, float | Decimal], weights: Dict[str, float | Decimal]) -> Decimal:
    relevance = Decimal("0")

    for element_name, element_value in element_values.items():
        weight = weights.get(element_name, Decimal("0"))
        relevance += decimal_from_literal(weight) * decimal_from_literal(element_value)

    return relevance


def main() -> None:
    if not TTL_PATH.exists():
        raise FileNotFoundError(f"TTL file not found: {TTL_PATH}. Run create_theseus_ontology.py first.")

    graph = Graph()
    graph.parse(TTL_PATH, format="turtle")

    element_values = get_element_values(graph)
    vectors = ["W_Marinheiro_Navegacao", "W_Historiador_Preservacao"]

    print("Elements from S(I_ship) and their ontological values v(p_i):")
    for element_name, value in element_values.items():
        print(f"- {element_name}: {value}")

    print("\nRel_prag(I,A,C) results:")
    for vector_name in vectors:
        _, weights = get_vector_weights(graph, vector_name)
        relevance = calculate_relevance(element_values, weights)
        print(f"- {vector_name}: {relevance}")

    print("\nInterpretation:")
    print("- The sailor profile prioritizes structure and navigation capacity.")
    print("- The historian profile prioritizes provenance, historical value, and monument role.")
    print("- Ontological instance remains stable; epistemic-pragmatic weighting changes.")


if __name__ == "__main__":
    main()
