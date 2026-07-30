"""RDF/OWL repository for S(I) in Equations 1 and 9."""

from __future__ import annotations

from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS

from .exceptions import OntologyNotFoundError
from .models import Descriptor, OntologyEntity

EX = Namespace("https://example.org/epm/theseus#")


class OntologyRepository:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self._cache: dict[str, Graph] = {}

    def _path_for(self, ontology_id: str) -> Path:
        return self.data_dir / f"{ontology_id}_ontology.ttl"

    def load_graph(self, ontology_id: str) -> Graph:
        if ontology_id in self._cache:
            return self._cache[ontology_id]
        path = self._path_for(ontology_id)
        if not path.exists():
            raise OntologyNotFoundError(f"Ontology '{ontology_id}' not found at {path}.")
        graph = Graph()
        graph.parse(path, format="turtle")
        self._cache[ontology_id] = graph
        return graph

    def get_entity(self, ontology_id: str, entity_id: str) -> OntologyEntity:
        graph = self.load_graph(ontology_id)
        entity_iri = EX[entity_id]
        if not any(graph.triples((entity_iri, RDF.type, None))):
            raise OntologyNotFoundError(f"Entity '{entity_id}' was not found in ontology '{ontology_id}'.")

        descriptors: list[Descriptor] = []
        for descriptor_iri in graph.objects(entity_iri, EX.hasDescriptor):
            descriptor_id = str(descriptor_iri).split("#")[-1]
            label = str(next(graph.objects(descriptor_iri, RDFS.label), descriptor_id))
            description = str(next(graph.objects(descriptor_iri, RDFS.comment), ""))
            descriptor_type = next(graph.objects(descriptor_iri, RDF.type), None)
            if descriptor_type is None:
                raise OntologyNotFoundError(f"Descriptor '{descriptor_id}' has no explicit OWL type.")
            descriptor_type_iri = str(descriptor_type)
            descriptor_kind = descriptor_type_iri.rsplit("#", 1)[-1]
            descriptors.append(
                Descriptor(
                    id=descriptor_id,
                    label=label,
                    description=description,
                    descriptor_kind=descriptor_kind,
                    descriptor_type_iri=descriptor_type_iri,
                )
            )

        if not descriptors:
            raise OntologyNotFoundError(
                f"Entity '{entity_id}' has no descriptors connected through epm:hasDescriptor."
            )

        return OntologyEntity(
            ontology_id=ontology_id,
            entity_id=entity_id,
            label=str(next(graph.objects(entity_iri, RDFS.label), entity_id)),
            description=str(next(graph.objects(entity_iri, RDFS.comment), "")),
            descriptors=sorted(descriptors, key=lambda item: item.id),
        )
