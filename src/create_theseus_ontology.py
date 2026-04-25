"""
Generates the Ship of Theseus base ontology in Turtle (.ttl).

Goal:
- Keep ONLY the entity's stable ontological structure.
- Do not include agent interpretive data (sailor, historian, etc.)
  inside the ontology.

This way, the ontology serves as a shared base for all examples.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Iterable

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, XSD

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = BASE_DIR / "data" / "theseus_ontology.ttl"

EX = Namespace("https://example.org/theseus#")
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_")


@dataclass(frozen=True)
class OntologicalElement:
    """Represents a p_i element belonging to S(I_ship)."""

    iri_name: str
    label: str
    comment: str
    value: Decimal = Decimal("1.0")
    is_role: bool = False


def add_label_comment(graph: Graph, subject, label: str, comment: str | None = None) -> None:
    graph.add((subject, RDFS.label, Literal(label, lang="en")))
    if comment:
        graph.add((subject, RDFS.comment, Literal(comment, lang="en")))


def add_classes(graph: Graph) -> None:
    classes = {
        EX.OntologicalInstance: ("Ontological instance", None),
        EX.MaterialEntity: (
            "Material entity",
            "Simplified class compatible with reading as a material entity/independent continuant.",
        ),
        EX.Ship: ("Ship", None),
        EX.OntologicalElement: (
            "Ontologically grounded element",
            "Descriptive component of the instance, such as quality, disposition, function, historical origin, or contextual role.",
        ),
        EX.Role: (
            "Role",
            "Condition or function contextually attributed to an entity without changing its ontological base.",
        ),
    }

    for class_iri, (label, comment) in classes.items():
        graph.add((class_iri, RDF.type, OWL.Class))
        add_label_comment(graph, class_iri, label, comment)

    graph.add((EX.MaterialEntity, RDFS.subClassOf, EX.OntologicalInstance))
    graph.add((EX.Ship, RDFS.subClassOf, EX.MaterialEntity))
    graph.add((EX.Role, RDFS.subClassOf, EX.OntologicalElement))


def add_properties(graph: Graph) -> None:
    graph.add((EX.hasElement, RDF.type, OWL.ObjectProperty))
    graph.add((EX.hasElement, RDFS.domain, EX.OntologicalInstance))
    graph.add((EX.hasElement, RDFS.range, EX.OntologicalElement))
    add_label_comment(graph, EX.hasElement, "has element")

    graph.add((EX.elementValue, RDF.type, OWL.DatatypeProperty))
    graph.add((EX.elementValue, RDFS.domain, EX.OntologicalElement))
    graph.add((EX.elementValue, RDFS.range, XSD.decimal))
    add_label_comment(graph, EX.elementValue, "element value")


def default_elements() -> list[OntologicalElement]:
    return [
        OntologicalElement("p_material", "Material composition", "Aspect related to the physical parts and material substrate of the ship."),
        OntologicalElement("p_estrutura", "Structural organization", "Aspect related to the ship's formal configuration and organization."),
        OntologicalElement("p_flutuar", "Disposition to float and navigate", "Realizable disposition associated with floating and navigation capability."),
        OntologicalElement("p_origem", "Origin and provenance", "Aspect related to the entity's origin, provenance, and historical continuity."),
        OntologicalElement("p_valor_historico", "Historical value", "Aspect related to the entity's historical, symbolic, and memorial relevance."),
        OntologicalElement(
            "p_papel_monumento",
            "Monument role",
            "Role contextually attributed to the ship in historical preservation practices.",
            is_role=True,
        ),
    ]


def add_theseus_instance(graph: Graph, elements: Iterable[OntologicalElement]) -> None:
    ship = EX.TheseusShip
    graph.add((ship, RDF.type, EX.Ship))
    add_label_comment(
        graph,
        ship,
        "Ship of Theseus",
        "Material instance with stable ontological structure used as a base for external pragmatic interpretations.",
    )

    for element in elements:
        element_iri = EX[element.iri_name]
        graph.add((element_iri, RDF.type, EX.Role if element.is_role else EX.OntologicalElement))
        add_label_comment(graph, element_iri, element.label, element.comment)
        graph.add((element_iri, EX.elementValue, Literal(element.value, datatype=XSD.decimal)))
        graph.add((ship, EX.hasElement, element_iri))


def build_graph() -> Graph:
    graph = Graph()
    graph.bind("", EX)
    graph.bind("bfo", BFO)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("owl", OWL)
    graph.bind("xsd", XSD)

    graph.add((EX.TheseusOntology, RDF.type, OWL.Ontology))
    add_label_comment(
        graph,
        EX.TheseusOntology,
        "Ship of Theseus base ontology",
        "Simplified ontology representing only the stable structure S(I_ship).",
    )

    add_classes(graph)
    add_properties(graph)
    add_theseus_instance(graph, default_elements())
    return graph


def main() -> None:
    graph = build_graph()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(OUTPUT_PATH), format="turtle")
    print(f"Ontology generated at: {OUTPUT_PATH}")
    print(f"Total RDF triples: {len(graph)}")


if __name__ == "__main__":
    main()
