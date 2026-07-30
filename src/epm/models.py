"""Typed contracts for the formal components of the Epistemic-Pragmatic Model."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

NonBlankString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
UnitFloat = Annotated[float, Field(ge=0.0, le=1.0)]


class Agent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: NonBlankString
    label: NonBlankString
    kind: Literal["human", "institution", "computational_system", "hybrid"]


class Context(BaseModel):
    """Minimal task-oriented representation C=<g,t,e,r,n>."""

    model_config = ConfigDict(extra="forbid")

    goal: NonBlankString
    temporal_scope: NonBlankString
    environment: NonBlankString
    roles: list[NonBlankString] = Field(min_length=1)
    norms: list[NonBlankString] = Field(min_length=1)


class ProvenanceRecord(BaseModel):
    """Operational representation of Pi_W."""

    model_config = ConfigDict(extra="forbid")

    source: NonBlankString
    method: NonBlankString
    evidence: list[NonBlankString] = Field(min_length=1)
    timestamp: datetime
    version: NonBlankString
    empirically_validated: bool = False


class InteractionRule(BaseModel):
    """A context-bound interaction used by the rule-aware aggregation strategy."""

    model_config = ConfigDict(extra="forbid")

    rule_id: NonBlankString
    kind: Literal["synergy", "redundancy", "veto", "requirement"]
    descriptors: list[NonBlankString] = Field(min_length=1)
    trigger: UnitFloat = 0.5
    coefficient: float = Field(default=0.1, ge=0.0, le=1.0)
    description: NonBlankString


class ComparatorSpec(BaseModel):
    """Descriptor-specific comparison function s_i."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["exact", "numeric_closeness", "string_ratio", "jaccard"]
    minimum: float | None = None
    maximum: float | None = None

    @model_validator(mode="after")
    def validate_range(self) -> "ComparatorSpec":
        if self.kind == "numeric_closeness":
            if self.minimum is None or self.maximum is None:
                raise ValueError("Numeric closeness requires explicit minimum and maximum values.")
            if self.maximum <= self.minimum:
                raise ValueError("Comparator maximum must be greater than minimum.")
        elif self.minimum is not None or self.maximum is not None:
            raise ValueError(f"Comparator '{self.kind}' does not use minimum or maximum values.")
        return self


class ValuationSpec(BaseModel):
    """Domain rule that turns an observed value into v_I(p_i) on [0,1]."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["normalized", "numeric_range", "categorical"]
    minimum: float | None = None
    maximum: float | None = None
    categories: dict[NonBlankString, UnitFloat] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_configuration(self) -> "ValuationSpec":
        if self.kind == "numeric_range":
            if self.minimum is None or self.maximum is None:
                raise ValueError("Numeric-range valuation requires explicit minimum and maximum values.")
            if self.maximum <= self.minimum:
                raise ValueError("Valuation maximum must be greater than minimum.")
            if self.categories:
                raise ValueError("Numeric-range valuation cannot define categories.")
        elif self.kind == "categorical":
            if not self.categories:
                raise ValueError("Categorical valuation requires at least one category.")
            if self.minimum is not None or self.maximum is not None:
                raise ValueError("Categorical valuation does not use minimum or maximum values.")
        elif self.minimum is not None or self.maximum is not None or self.categories:
            raise ValueError("Normalized valuation does not accept range or category settings.")
        return self


class AggregationSpec(BaseModel):
    """The explicit, context-bound instantiation of Agg_C."""

    model_config = ConfigDict(extra="forbid")

    strategy: Literal["weighted_average", "weighted_sum", "rule_aware"]
    rules: list[InteractionRule] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_rules(self) -> "AggregationSpec":
        if self.strategy == "rule_aware" and not self.rules:
            raise ValueError("Rule-aware aggregation requires at least one interaction rule.")
        if self.strategy != "rule_aware" and self.rules:
            raise ValueError("Interaction rules are only valid with rule-aware aggregation.")
        return self


class EvaluationConfiguration(BaseModel):
    """Versioned realization of v, s, Agg_C, and the operational threshold."""

    model_config = ConfigDict(extra="forbid")

    version: NonBlankString
    valuations: dict[NonBlankString, ValuationSpec]
    comparators: dict[NonBlankString, ComparatorSpec]
    relevance_aggregation: AggregationSpec
    similarity_aggregation: AggregationSpec
    similarity_threshold: UnitFloat


class WeightingPolicy(BaseModel):
    """W(A,C), Pi_W, and the versioned operators used with that vector."""

    model_config = ConfigDict(extra="forbid")

    policy_id: NonBlankString
    ontology_id: NonBlankString
    agent: Agent
    context: Context
    interpretive_role: NonBlankString
    weights: dict[NonBlankString, UnitFloat]
    provenance: ProvenanceRecord
    evaluation: EvaluationConfiguration
    notes: list[NonBlankString] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_meaningful_weights(self) -> "WeightingPolicy":
        if not self.weights:
            raise ValueError("A weighting policy must contain at least one descriptor weight.")
        if not any(weight > 0.0 for weight in self.weights.values()):
            raise ValueError("A weighting policy must assign positive relevance to at least one descriptor.")
        return self


class Descriptor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: NonBlankString
    label: NonBlankString
    description: NonBlankString
    descriptor_kind: NonBlankString
    descriptor_type_iri: NonBlankString


class OntologyEntity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ontology_id: NonBlankString
    entity_id: NonBlankString
    label: NonBlankString
    description: NonBlankString
    descriptors: list[Descriptor] = Field(min_length=1)


class RelevanceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ontology_id: NonBlankString = "theseus"
    entity_id: NonBlankString = "TheseusShip"
    policy_id: NonBlankString
    # Observations remain outside S(I); the policy defines how they become v_I(p_i).
    descriptor_values: dict[NonBlankString, Any]


class Contribution(BaseModel):
    descriptor_id: str
    label: str
    observed_value: Any
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
    evaluation_version: str
    score: float
    raw_score: float
    score_is_normalized: bool
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

    ontology_id: NonBlankString = "theseus"
    entity_id: NonBlankString = "TheseusShip"
    policy_id: NonBlankString
    left_record_id: NonBlankString
    right_record_id: NonBlankString
    left_values: dict[NonBlankString, Any]
    right_values: dict[NonBlankString, Any]


class SimilarityContribution(BaseModel):
    descriptor_id: str
    label: str
    left_value: Any
    right_value: Any
    comparator: ComparatorSpec
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
    evaluation_version: str
    left_record_id: str
    right_record_id: str
    score: float
    raw_score: float
    score_is_normalized: Literal[True] = True
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
