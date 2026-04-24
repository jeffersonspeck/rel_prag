"""
Gera a ontologia-base do Navio de Teseu em Turtle (.ttl).

Objetivo:
- Manter SOMENTE a estrutura ontológica estável da entidade.
- Não incluir dados interpretativos de agentes (marinheiro, historiador etc.)
  dentro da ontologia.

Assim, a ontologia funciona como base compartilhada para todos os exemplos.
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
    """Representa um elemento p_i pertencente a S(I_navio)."""

    iri_name: str
    label: str
    comment: str
    value: Decimal = Decimal("1.0")
    is_role: bool = False


def add_label_comment(graph: Graph, subject, label: str, comment: str | None = None) -> None:
    graph.add((subject, RDFS.label, Literal(label, lang="pt")))
    if comment:
        graph.add((subject, RDFS.comment, Literal(comment, lang="pt")))


def add_classes(graph: Graph) -> None:
    classes = {
        EX.OntologicalInstance: ("Instância ontológica", None),
        EX.MaterialEntity: (
            "Entidade material",
            "Classe simplificada compatível com a leitura de entidade material/continuante independente.",
        ),
        EX.Ship: ("Navio", None),
        EX.OntologicalElement: (
            "Elemento ontologicamente ancorado",
            "Componente descritivo da instância, como qualidade, disposição, função, origem histórica ou papel contextual.",
        ),
        EX.Role: (
            "Papel",
            "Condição ou função contextualmente atribuída a uma entidade sem alterar sua base ontológica.",
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
    add_label_comment(graph, EX.hasElement, "tem elemento")

    graph.add((EX.elementValue, RDF.type, OWL.DatatypeProperty))
    graph.add((EX.elementValue, RDFS.domain, EX.OntologicalElement))
    graph.add((EX.elementValue, RDFS.range, XSD.decimal))
    add_label_comment(graph, EX.elementValue, "valor do elemento")


def default_elements() -> list[OntologicalElement]:
    return [
        OntologicalElement("p_material", "Composição material", "Aspecto relativo às partes físicas e ao substrato material do navio."),
        OntologicalElement("p_estrutura", "Organização estrutural", "Aspecto relativo à configuração formal e organização do navio."),
        OntologicalElement("p_flutuar", "Disposição para flutuar e navegar", "Disposição realizável associada à capacidade de flutuação e navegação."),
        OntologicalElement("p_origem", "Origem e procedência", "Aspecto relativo à origem, procedência e continuidade histórica da entidade."),
        OntologicalElement("p_valor_historico", "Valor histórico", "Aspecto relativo à relevância histórica, simbólica e memorial da entidade."),
        OntologicalElement(
            "p_papel_monumento",
            "Papel de monumento",
            "Papel contextualmente atribuído ao navio em práticas de preservação histórica.",
            is_role=True,
        ),
    ]


def add_theseus_instance(graph: Graph, elements: Iterable[OntologicalElement]) -> None:
    ship = EX.TheseusShip
    graph.add((ship, RDF.type, EX.Ship))
    add_label_comment(
        graph,
        ship,
        "Navio de Teseu",
        "Instância material com estrutura ontológica estável usada como base para interpretações pragmáticas externas.",
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
        "Ontologia-base do Navio de Teseu",
        "Ontologia simplificada para representar apenas a estrutura estável S(I_navio).",
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
