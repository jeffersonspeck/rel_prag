"""Typed contracts for policies, context, provenance, and model outputs."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

UnitFloat = Annotated[float, Field(ge=0.0, le=1.0)]


class Agent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    label: str
    kind: Literal["human", "institution", "computational_system", "hybrid"]


class Context(BaseModel):
    """Minimal task-oriented representation C=<g,t,e,r,n>."""

    model_config = ConfigDict(extra="forbid")

    goal: str
    temporal_scope: str
    environment: str
    roles: list[str] = Field(default_factory=list)
    norms: list[str] = Field(default_factory=list)


class ProvenanceRecord(BaseModel):
    """Operational representation of Pi_W."""

    model_config = ConfigDict(extra="forbid")

    source: str
    method: str
    evidence: list[str] = Field(default_factory=list)
    timestamp: datetime
    version: str
    empirically_validated: bool = False


class WeightingPolicy(BaseModel):
    """W(A,C) plus the provenance record required for auditing."""

    model_config = ConfigDict(extra="forbid")

    policy_id: str
    ontology_id: str
    agent: Agent
    context: Context
    interpretive_role: str
    weights: dict[str, UnitFloat]
    provenance: ProvenanceRecord
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_weights(self) -> "WeightingPolicy":
        if not self.weights:
            raise ValueError("A weighting policy must contain at least one descriptor weight.")
        return self


class Descriptor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    label: str
    description: str
    descriptor_kind: str
    default_value: UnitFloat = 1.0


class OntologyEntity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ontology_id: str
    entity_id: str
    label: str
    description: str
    descriptors: list[Descriptor]


class InteractionRule(BaseModel):
    """Optional rule used by the rule-aware aggregation strategy."""

    model_config = ConfigDict(extra="forbid")

    rule_id: str
    kind: Literal["synergy", "redundancy", "veto", "requirement"]
    descriptors: list[str] = Field(min_length=1)
    trigger: UnitFloat = 0.5
    coefficient: float = Field(default=0.1, ge=0.0, le=1.0)
    description: str


class ComparatorSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["exact", "numeric_closeness", "string_ratio", "jaccard"] = "numeric_closeness"
    minimum: float | None = None
    maximum: float | None = None

    @model_validator(mode="after")
    def validate_range(self) -> "ComparatorSpec":
        if self.kind == "numeric_closeness":
            if self.minimum is None:
                self.minimum = 0.0
            if self.maximum is None:
                self.maximum = 1.0
            if self.maximum <= self.minimum:
                raise ValueError("Comparator maximum must be greater than minimum.")
        return self


class RelevanceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ontology_id: str = "theseus"
    entity_id: str = "TheseusShip"
    policy_id: str
    descriptor_values: dict[str, UnitFloat] | None = None
    aggregator: Literal["weighted_average", "weighted_sum", "rule_aware"] = "weighted_average"
    interaction_rules: list[InteractionRule] = Field(default_factory=list)


class Contribution(BaseModel):
    descriptor_id: str
    label: str
    value: float
    weight: float
    weighted_contribution: float
    normalized_contribution: float


class RelevanceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    measure_type: Literal["unary_contextual_relevance"] = "unary_contextual_relevance"
    ontology_id: str
    entity_id: str
    policy_id: str
    score: float
    raw_score: float
    aggregator: str
    contributions: list[Contribution]
    agent: Agent
    context: Context
    interpretive_role: str
    provenance: ProvenanceRecord
    applied_rules: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SimilarityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ontology_id: str = "theseus"
    entity_id: str = "TheseusShip"
    policy_id: str
    left_record_id: str
    right_record_id: str
    left_values: dict[str, Any]
    right_values: dict[str, Any]
    comparators: dict[str, ComparatorSpec] = Field(default_factory=dict)
    threshold: UnitFloat = 0.85
    aggregator: Literal["weighted_average", "weighted_sum", "rule_aware"] = "weighted_average"
    interaction_rules: list[InteractionRule] = Field(default_factory=list)


class SimilarityContribution(BaseModel):
    descriptor_id: str
    label: str
    left_value: Any
    right_value: Any
    similarity: float
    weight: float
    weighted_contribution: float
    normalized_contribution: float


class SimilarityResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    measure_type: Literal["binary_contextual_similarity"] = "binary_contextual_similarity"
    ontology_id: str
    entity_id: str
    policy_id: str
    left_record_id: str
    right_record_id: str
    score: float
    raw_score: float
    threshold: float
    operational_continuity_supported: bool
    numerical_identity_claimed: Literal[False] = False
    aggregator: str
    contributions: list[SimilarityContribution]
    agent: Agent
    context: Context
    provenance: ProvenanceRecord
    applied_rules: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
