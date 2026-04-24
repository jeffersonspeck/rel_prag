"""
Gera a ontologia epistêmico-pragmática do Navio de Teseu em Turtle (.ttl).

O script implementa os elementos centrais formulados no texto:

- Instância ontológica estável I_navio.
- Estrutura S(I_navio), composta por elementos ontologicamente ancorados.
- Agentes A: marinheiro e historiador.
- Contextos C: navegação e preservação histórica.
- Vetores W(A,C), com pesos no intervalo [0,1].

Dependência:
    pip install rdflib

Execução:
    python src/create_theseus_ontology.py
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Dict, Iterable

from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, XSD


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = BASE_DIR / "data" / "theseus_ontology.ttl"

EX = Namespace("https://example.org/theseus#")
BFO = Namespace("http://purl.obolibrary.org/obo/BFO_")


@dataclass(frozen=True)
class OntologicalElement:
    """Representa um elemento p_i pertencente a S(I)."""

    iri_name: str
    label: str
    comment: str
    value: Decimal = Decimal("1.0")
    is_role: bool = False


@dataclass(frozen=True)
class Agent:
    iri_name: str
    label: str
    comment: str


@dataclass(frozen=True)
class Context:
    iri_name: str
    label: str


@dataclass(frozen=True)
class WeightVector:
    """Representa W(A,C), isto é, um vetor de ponderação epistêmico-pragmática."""

    iri_name: str
    label: str
    agent: Agent
    context: Context
    weights: Dict[str, Decimal]


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
        EX.Agent: ("Agente", "Entidade que interpreta, consulta, consome ou opera sobre a ontologia."),
        EX.Context: ("Contexto", "Cenário de uso em que certos aspectos da entidade se tornam mais ou menos relevantes."),
        EX.Role: (
            "Papel",
            "Condição ou função contextualmente atribuída a uma entidade sem alterar sua base ontológica.",
        ),
        EX.WeightVector: (
            "Vetor de ponderação",
            "Vetor W(A,C) que representa a ponderação epistêmico-pragmática definida por agente e contexto.",
        ),
        EX.WeightAssignment: (
            "Atribuição de peso",
            "Associação entre um elemento ontológico e seu peso de relevância para um agente em um contexto.",
        ),
    }

    for class_iri, (label, comment) in classes.items():
        graph.add((class_iri, RDF.type, OWL.Class))
        add_label_comment(graph, class_iri, label, comment)

    graph.add((EX.MaterialEntity, RDFS.subClassOf, EX.OntologicalInstance))
    graph.add((EX.Ship, RDFS.subClassOf, EX.MaterialEntity))
    graph.add((EX.Role, RDFS.subClassOf, EX.OntologicalElement))


def add_properties(graph: Graph) -> None:
    object_properties = [
        (EX.hasElement, EX.OntologicalInstance, EX.OntologicalElement, "tem elemento"),
        (EX.interpretedBy, EX.WeightVector, EX.Agent, "interpretado por"),
        (EX.inContext, EX.WeightVector, EX.Context, "em contexto"),
        (EX.aboutInstance, EX.WeightVector, EX.OntologicalInstance, "sobre instância"),
        (EX.hasWeightAssignment, EX.WeightVector, EX.WeightAssignment, "tem atribuição de peso"),
        (EX.forElement, EX.WeightAssignment, EX.OntologicalElement, "para elemento"),
    ]

    for prop, domain, range_, label in object_properties:
        graph.add((prop, RDF.type, OWL.ObjectProperty))
        graph.add((prop, RDFS.domain, domain))
        graph.add((prop, RDFS.range, range_))
        add_label_comment(graph, prop, label)

    datatype_properties = [
        (EX.weightValue, EX.WeightAssignment, XSD.decimal, "valor do peso"),
        (EX.elementValue, EX.OntologicalElement, XSD.decimal, "valor do elemento"),
    ]

    for prop, domain, range_, label in datatype_properties:
        graph.add((prop, RDF.type, OWL.DatatypeProperty))
        graph.add((prop, RDFS.domain, domain))
        graph.add((prop, RDFS.range, range_))
        add_label_comment(graph, prop, label)


def default_elements() -> list[OntologicalElement]:
    return [
        OntologicalElement(
            "p_material",
            "Composição material",
            "Aspecto relativo às partes físicas e ao substrato material do navio.",
        ),
        OntologicalElement(
            "p_estrutura",
            "Organização estrutural",
            "Aspecto relativo à configuração formal e organização do navio.",
        ),
        OntologicalElement(
            "p_flutuar",
            "Disposição para flutuar e navegar",
            "Disposição realizável associada à capacidade de flutuação e navegação.",
        ),
        OntologicalElement(
            "p_origem",
            "Origem e procedência",
            "Aspecto relativo à origem, procedência e continuidade histórica da entidade.",
        ),
        OntologicalElement(
            "p_valor_historico",
            "Valor histórico",
            "Aspecto relativo à relevância histórica, simbólica e memorial da entidade.",
        ),
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
        "Instância material cuja estrutura ontológica estável é interpretada por diferentes agentes e contextos.",
    )

    for element in elements:
        element_iri = EX[element.iri_name]
        graph.add((element_iri, RDF.type, EX.Role if element.is_role else EX.OntologicalElement))
        add_label_comment(graph, element_iri, element.label, element.comment)
        graph.add((element_iri, EX.elementValue, Literal(element.value, datatype=XSD.decimal)))
        graph.add((ship, EX.hasElement, element_iri))


def add_agents_contexts_and_vectors(graph: Graph, elements: list[OntologicalElement]) -> None:
    marinheiro = Agent("Marinheiro", "Marinheiro", "Agente que interpreta o navio prioritariamente como embarcação funcional.")
    historiador = Agent("Historiador", "Historiador", "Agente que interpreta o navio prioritariamente como objeto de preservação histórica.")

    navegacao = Context("ContextoNavegacao", "Contexto de navegação")
    preservacao = Context("ContextoPreservacaoHistorica", "Contexto de preservação histórica")

    for agent in [marinheiro, historiador]:
        iri = EX[agent.iri_name]
        graph.add((iri, RDF.type, EX.Agent))
        add_label_comment(graph, iri, agent.label, agent.comment)

    for context in [navegacao, preservacao]:
        iri = EX[context.iri_name]
        graph.add((iri, RDF.type, EX.Context))
        add_label_comment(graph, iri, context.label)

    vectors = [
        WeightVector(
            "W_Marinheiro_Navegacao",
            "W(A_mar, C_nav)",
            marinheiro,
            navegacao,
            {
                "p_material": Decimal("0.2"),
                "p_estrutura": Decimal("0.8"),
                "p_flutuar": Decimal("1.0"),
                "p_origem": Decimal("0.1"),
                "p_valor_historico": Decimal("0.1"),
                "p_papel_monumento": Decimal("0.0"),
            },
        ),
        WeightVector(
            "W_Historiador_Preservacao",
            "W(A_hist, C_hist)",
            historiador,
            preservacao,
            {
                "p_material": Decimal("0.9"),
                "p_estrutura": Decimal("0.4"),
                "p_flutuar": Decimal("0.1"),
                "p_origem": Decimal("1.0"),
                "p_valor_historico": Decimal("1.0"),
                "p_papel_monumento": Decimal("0.9"),
            },
        ),
    ]

    element_names = {e.iri_name for e in elements}

    for vector in vectors:
        vector_iri = EX[vector.iri_name]
        graph.add((vector_iri, RDF.type, EX.WeightVector))
        add_label_comment(graph, vector_iri, vector.label)
        graph.add((vector_iri, EX.aboutInstance, EX.TheseusShip))
        graph.add((vector_iri, EX.interpretedBy, EX[vector.agent.iri_name]))
        graph.add((vector_iri, EX.inContext, EX[vector.context.iri_name]))

        for element_name, weight in vector.weights.items():
            if element_name not in element_names:
                raise ValueError(f"Elemento desconhecido no vetor {vector.iri_name}: {element_name}")
            if not (Decimal("0") <= weight <= Decimal("1")):
                raise ValueError(f"Peso fora do intervalo [0,1]: {weight}")

            assignment_iri = EX[f"{vector.iri_name}_{element_name}"]
            graph.add((assignment_iri, RDF.type, EX.WeightAssignment))
            graph.add((assignment_iri, EX.forElement, EX[element_name]))
            graph.add((assignment_iri, EX.weightValue, Literal(weight, datatype=XSD.decimal)))
            graph.add((vector_iri, EX.hasWeightAssignment, assignment_iri))


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
        "Ontologia epistêmico-pragmática do Navio de Teseu",
        "Ontologia simplificada para representar a distinção entre estrutura ontológica estável e ponderação epistêmico-pragmática por agente e contexto.",
    )

    add_classes(graph)
    add_properties(graph)
    elements = default_elements()
    add_theseus_instance(graph, elements)
    add_agents_contexts_and_vectors(graph, elements)
    return graph


def main() -> None:
    graph = build_graph()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(OUTPUT_PATH), format="turtle")
    print(f"Ontology generated at: {OUTPUT_PATH}")
    print(f"Total RDF triples: {len(graph)}")


if __name__ == "__main__":
    main()
