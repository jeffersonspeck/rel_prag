"""Generate the stable Ship of Theseus ontology in Turtle.

Agents, contexts, weights, provenance records, and decisions are intentionally
kept outside the ontology. They belong to the epistemic-pragmatic policy layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, SKOS, XSD

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "theseus_ontology.ttl"
EX = Namespace("https://example.org/epm/theseus#")
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_")


@dataclass(frozen=True)
class DescriptorDefinition:
    iri_name: str
    label: str
    description: str
    kind: str
    default_value: Decimal = Decimal("1.0")


DESCRIPTORS = [
    DescriptorDefinition("p_material", "Material composition", "Physical parts and material substrate of the ship.", "part/provenance"),
    DescriptorDefinition("p_structure", "Structural organization", "Formal configuration and organization of the ship.", "structure"),
    DescriptorDefinition("p_float", "Disposition to float and navigate", "Realizable disposition related to floating and navigation.", "disposition"),
    DescriptorDefinition("p_origin", "Origin and provenance", "Origin, provenance, and historical continuity.", "provenance"),
    DescriptorDefinition("p_historical_value", "Historical value", "Historical, symbolic, and memorial relevance.", "quality"),
    DescriptorDefinition("p_monument_role", "Monument role", "Context-dependent role in preservation practices.", "role"),
]


def add_label_comment(graph: Graph, subject, label: str, description: str = "") -> None:
    graph.add((subject, RDFS.label, Literal(label, lang="en")))
    if description:
        graph.add((subject, RDFS.comment, Literal(description, lang="en")))


def build_graph() -> Graph:
    graph = Graph()
    graph.bind("epm", EX)
    graph.bind("owl", OWL)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("skos", SKOS)
    graph.bind("xsd", XSD)

    graph.add((EX.TheseusOntology, RDF.type, OWL.Ontology))
    add_label_comment(
        graph,
        EX.TheseusOntology,
        "Ship of Theseus stable ontology",
        "Reference ontology containing only the ontologically anchored descriptor schema S(I).",
    )

    for class_iri, label, description in [
        (EX.OntologicalInstance, "Ontological instance", "Entity described by an ontology-grounded descriptor schema."),
        (EX.MaterialEntity, "Material entity", "Domain class used for physical entities in this example."),
        (EX.Ship, "Ship", "Material artifact capable of realizing navigation-related dispositions."),
        (EX.Descriptor, "Typed descriptor", "Ontology-grounded aspect available to the policy layer."),
    ]:
        graph.add((class_iri, RDF.type, OWL.Class))
        add_label_comment(graph, class_iri, label, description)

    graph.add((EX.MaterialEntity, RDFS.subClassOf, EX.OntologicalInstance))
    graph.add((EX.Ship, RDFS.subClassOf, EX.MaterialEntity))
    # A deliberately weak alignment avoids making the entire implementation
    # dependent on a specific foundational ontology.
    graph.add((EX.MaterialEntity, SKOS.closeMatch, BFO["0000040"]))

    graph.add((EX.hasDescriptor, RDF.type, OWL.ObjectProperty))
    graph.add((EX.hasDescriptor, RDFS.domain, EX.OntologicalInstance))
    graph.add((EX.hasDescriptor, RDFS.range, EX.Descriptor))
    graph.add((EX.defaultValue, RDF.type, OWL.DatatypeProperty))
    graph.add((EX.defaultValue, RDFS.range, XSD.decimal))
    graph.add((EX.descriptorKind, RDF.type, OWL.DatatypeProperty))
    graph.add((EX.descriptorKind, RDFS.range, XSD.string))

    graph.add((EX.TheseusShip, RDF.type, EX.Ship))
    add_label_comment(
        graph,
        EX.TheseusShip,
        "Ship of Theseus",
        "Material instance used by independent systems over the same stable ontology.",
    )

    for descriptor in DESCRIPTORS:
        iri = EX[descriptor.iri_name]
        graph.add((iri, RDF.type, EX.Descriptor))
        add_label_comment(graph, iri, descriptor.label, descriptor.description)
        graph.add((iri, EX.descriptorKind, Literal(descriptor.kind)))
        graph.add((iri, EX.defaultValue, Literal(descriptor.default_value, datatype=XSD.decimal)))
        graph.add((EX.TheseusShip, EX.hasDescriptor, iri))

    return graph


def main() -> None:
    graph = build_graph()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(OUTPUT), format="turtle")
    print(f"Ontology generated at: {OUTPUT}")
    print(f"RDF triples: {len(graph)}")


if __name__ == "__main__":
    main()
