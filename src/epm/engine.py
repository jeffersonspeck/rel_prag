"""Core execution engine for unary relevance and binary similarity."""

from __future__ import annotations

from .aggregators import WeightedInput, aggregate
from .comparators import compare
from .exceptions import AggregationError
from .models import (
    Contribution,
    OntologyEntity,
    RelevanceRequest,
    RelevanceResponse,
    SimilarityContribution,
    SimilarityRequest,
    SimilarityResponse,
    WeightingPolicy,
)
from .valuations import valuate


class EpistemicPragmaticEngine:
    @staticmethod
    def _require_complete_schema(
        entity: OntologyEntity,
        supplied: dict[str, object],
        record_name: str,
    ) -> None:
        """Keep every valuation and comparison anchored in S(I)."""
        required = {descriptor.id for descriptor in entity.descriptors}
        present = set(supplied)
        missing = required - present
        unknown = present - required
        if missing or unknown:
            raise ValueError(
                f"{record_name} must use the complete ontology-grounded descriptor schema. "
                f"Missing={sorted(missing)} Unknown={sorted(unknown)}"
            )

    def relevance(
        self,
        request: RelevanceRequest,
        entity: OntologyEntity,
        policy: WeightingPolicy,
    ) -> RelevanceResponse:
        self._require_complete_schema(entity, request.descriptor_values, "Relevance observations")
        descriptor_by_id = {descriptor.id: descriptor for descriptor in entity.descriptors}
        aggregation = policy.evaluation.relevance_aggregation

        valued: dict[str, float] = {}
        for descriptor_id, observed in request.descriptor_values.items():
            try:
                valued[descriptor_id] = valuate(
                    observed,
                    policy.evaluation.valuations[descriptor_id],
                )
            except ValueError as exc:
                raise ValueError(f"Invalid observation for descriptor '{descriptor_id}': {exc}") from exc

        # Article Equation 6:
        # Rel_prag(I,A,C) = Agg_C({(w_i(A,C), v_I(p_i))}_{i=1}^n).
        inputs = [
            WeightedInput(descriptor_id=descriptor_id, value=valued[descriptor_id], weight=weight)
            for descriptor_id, weight in policy.weights.items()
        ]
        result = aggregate(aggregation.strategy, inputs, aggregation.rules)
        denominator = result.raw_score if result.raw_score else 0.0
        contributions = [
            Contribution(
                descriptor_id=item.descriptor_id,
                label=descriptor_by_id[item.descriptor_id].label,
                observed_value=request.descriptor_values[item.descriptor_id],
                value=item.value,
                weight=item.weight,
                weighted_contribution=round(item.weight * item.value, 6),
                normalized_contribution=round((item.weight * item.value) / denominator, 6) if denominator else 0.0,
            )
            for item in inputs
        ]
        warnings = [
            "The score expresses contextual relevance under the selected policy; it is not an ontological truth claim."
        ]
        if not policy.provenance.empirically_validated:
            warnings.append("The selected policy is illustrative or not yet empirically validated.")
        if aggregation.strategy == "weighted_sum":
            warnings.append(
                "The linear weighted sum assumes sufficiently comparable and approximately separable descriptor contributions."
            )
            if not result.normalized:
                warnings.append(
                    "This raw weighted sum is not normalized and must not be compared across contexts or against unit thresholds."
                )

        return RelevanceResponse(
            ontology_id=entity.ontology_id,
            entity_id=entity.entity_id,
            policy_id=policy.policy_id,
            evaluation_version=policy.evaluation.version,
            score=round(result.score, 6),
            raw_score=round(result.raw_score, 6),
            score_is_normalized=result.normalized,
            aggregator=aggregation.strategy,
            contributions=contributions,
            agent=policy.agent,
            context=policy.context,
            interpretive_role=policy.interpretive_role,
            provenance=policy.provenance,
            applied_rules=result.applied_rules,
            warnings=warnings,
        )

    def similarity(
        self,
        request: SimilarityRequest,
        entity: OntologyEntity,
        policy: WeightingPolicy,
    ) -> SimilarityResponse:
        self._require_complete_schema(entity, request.left_values, "Left similarity record")
        self._require_complete_schema(entity, request.right_values, "Right similarity record")
        descriptor_by_id = {descriptor.id: descriptor for descriptor in entity.descriptors}
        aggregation = policy.evaluation.similarity_aggregation

        # Article Equation 8:
        # Sim_prag(I',I'',A,C) =
        # Agg_C({(w_i(A,C), s_i(v_I'(p_i), v_I''(p_i)))}_{i=1}^n).
        inputs: list[WeightedInput] = []
        rows: list[tuple[str, float, float]] = []
        for descriptor_id, weight in policy.weights.items():
            spec = policy.evaluation.comparators[descriptor_id]
            similarity = compare(
                request.left_values[descriptor_id],
                request.right_values[descriptor_id],
                spec,
            )
            inputs.append(WeightedInput(descriptor_id=descriptor_id, value=similarity, weight=weight))
            rows.append((descriptor_id, similarity, weight))

        result = aggregate(aggregation.strategy, inputs, aggregation.rules)
        if not result.normalized:
            raise AggregationError(
                "Operational continuity requires a normalized similarity score. "
                "Use weighted_average, rule_aware, or a weighted_sum policy whose weights sum to one."
            )

        denominator = result.raw_score if result.raw_score else 0.0
        contributions = [
            SimilarityContribution(
                descriptor_id=descriptor_id,
                label=descriptor_by_id[descriptor_id].label,
                left_value=request.left_values[descriptor_id],
                right_value=request.right_values[descriptor_id],
                comparator=policy.evaluation.comparators[descriptor_id],
                similarity=round(similarity, 6),
                weight=weight,
                weighted_contribution=round(weight * similarity, 6),
                normalized_contribution=round((weight * similarity) / denominator, 6) if denominator else 0.0,
            )
            for descriptor_id, similarity, weight in rows
        ]
        warnings = [
            "Thresholded pairwise similarity supports an operational continuity decision, not numerical identity.",
            "The resulting continuity relation is not guaranteed to be transitive across a sequence of states.",
            "Longitudinal identity management should add lineage, provenance, or global continuity constraints.",
        ]
        if not policy.provenance.empirically_validated:
            warnings.append("The selected policy is illustrative or not yet empirically validated.")

        threshold = policy.evaluation.similarity_threshold
        # Equation 18 calls this ContextContinuitySupport. It remains an
        # operational, context-bound result and never a numerical identity claim.
        return SimilarityResponse(
            ontology_id=entity.ontology_id,
            entity_id=entity.entity_id,
            policy_id=policy.policy_id,
            evaluation_version=policy.evaluation.version,
            left_record_id=request.left_record_id,
            right_record_id=request.right_record_id,
            score=round(result.score, 6),
            raw_score=round(result.raw_score, 6),
            threshold=threshold,
            operational_continuity_supported=result.score >= threshold,
            aggregator=aggregation.strategy,
            contributions=contributions,
            agent=policy.agent,
            context=policy.context,
            provenance=policy.provenance,
            applied_rules=result.applied_rules,
            warnings=warnings,
        )
