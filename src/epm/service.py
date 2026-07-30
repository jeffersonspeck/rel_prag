"""Application service coordinating ontology, policy, engine, and audit."""

from __future__ import annotations

from .audit import AuditLogger
from .engine import EpistemicPragmaticEngine
from .models import RelevanceRequest, RelevanceResponse, SimilarityRequest, SimilarityResponse
from .ontology import OntologyRepository
from .policies import PolicyRepository


class EpistemicPragmaticService:
    def __init__(
        self,
        ontology_repository: OntologyRepository,
        policy_repository: PolicyRepository,
        audit_logger: AuditLogger,
        engine: EpistemicPragmaticEngine | None = None,
    ) -> None:
        self.ontology_repository = ontology_repository
        self.policy_repository = policy_repository
        self.audit_logger = audit_logger
        self.engine = engine or EpistemicPragmaticEngine()

    def relevance(self, request: RelevanceRequest) -> RelevanceResponse:
        entity = self.ontology_repository.get_entity(request.ontology_id, request.entity_id)
        policy = self.policy_repository.get(request.policy_id)
        self.policy_repository.validate_against_entity(policy, entity)
        response = self.engine.relevance(request, entity, policy)
        # A decision is reproducible only when its observations, policy, and
        # output are kept together. The policy carries W, v, s, Agg_C, and beta.
        self.audit_logger.record(
            "unary_contextual_relevance",
            {
                "request": request.model_dump(mode="json"),
                "policy": policy.model_dump(mode="json"),
                "response": response.model_dump(mode="json"),
            },
        )
        return response

    def similarity(self, request: SimilarityRequest) -> SimilarityResponse:
        entity = self.ontology_repository.get_entity(request.ontology_id, request.entity_id)
        policy = self.policy_repository.get(request.policy_id)
        self.policy_repository.validate_against_entity(policy, entity)
        response = self.engine.similarity(request, entity, policy)
        self.audit_logger.record(
            "binary_contextual_similarity",
            {
                "request": request.model_dump(mode="json"),
                "policy": policy.model_dump(mode="json"),
                "response": response.model_dump(mode="json"),
            },
        )
        return response
