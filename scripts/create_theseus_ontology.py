"""Generate the stable Ship of Theseus ontology in Turtle.

Agents, contexts, weights, provenance records, and decisions are intentionally
kept outside the ontology. They belong to the epistemic-pragmatic policy layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rdflib import Graph, Literal, Namespace, OWL, RDF, RDFS, SKOS

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "theseus_ontology.ttl"
EX = Namespace("https://example.org/epm/theseus#")
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_")


@dataclass(frozen=True)
class DescriptorDefinition:
    iri_name: str
    label: str
    description: str
    type_name: str


DESCRIPTORS = [
    DescriptorDefinition("p_material", "Material composition", "Physical parts and material substrate of the ship.", "PartDescriptor"),
    DescriptorDefinition("p_structure", "Structural organization", "Formal configuration and organization of the ship.", "StructuralDescriptor"),
    DescriptorDefinition("p_float", "Disposition to float and navigate", "Realizable disposition related to floating and navigation.", "DispositionDescriptor"),
    DescriptorDefinition("p_origin", "Origin and provenance", "Origin, provenance, and historical continuity.", "ProvenanceDescriptor"),
    DescriptorDefinition("p_historical_value", "Historical value", "Historical, symbolic, and memorial relevance.", "QualityDescriptor"),
    DescriptorDefinition("p_monument_role", "Monument role", "Context-dependent role in preservation practices.", "RoleDescriptor"),
]

DESCRIPTOR_TYPES = [
    ("PartDescriptor", "Part descriptor", "Descriptor concerning material parts or composition."),
    ("StructuralDescriptor", "Structural descriptor", "Descriptor concerning formal organization."),
    ("DispositionDescriptor", "Disposition descriptor", "Descriptor concerning a realizable disposition."),
    ("ProvenanceDescriptor", "Provenance descriptor", "Descriptor concerning origin or provenance."),
    ("QualityDescriptor", "Quality descriptor", "Descriptor concerning a quality of the entity."),
    ("RoleDescriptor", "Role descriptor", "Descriptor concerning a context-dependent role."),
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

    # Descriptor categories are OWL classes rather than string annotations.
    # This keeps heterogeneous aspects formally visible inside S(I).
    for type_name, label, description in DESCRIPTOR_TYPES:
        type_iri = EX[type_name]
        graph.add((type_iri, RDF.type, OWL.Class))
        graph.add((type_iri, RDFS.subClassOf, EX.Descriptor))
        add_label_comment(graph, type_iri, label, description)

    graph.add((EX.TheseusShip, RDF.type, EX.Ship))
    add_label_comment(
        graph,
        EX.TheseusShip,
        "Ship of Theseus",
        "Material instance used by independent systems over the same stable ontology.",
    )

    for descriptor in DESCRIPTORS:
        iri = EX[descriptor.iri_name]
        graph.add((iri, RDF.type, EX[descriptor.type_name]))
        add_label_comment(graph, iri, descriptor.label, descriptor.description)
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
