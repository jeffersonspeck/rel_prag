"""Core execution engine for unary relevance and binary similarity."""

from __future__ import annotations

from .aggregators import WeightedInput, aggregate
from .comparators import compare
from .models import (
    ComparatorSpec,
    Contribution,
    OntologyEntity,
    RelevanceRequest,
    RelevanceResponse,
    SimilarityContribution,
    SimilarityRequest,
    SimilarityResponse,
    WeightingPolicy,
)


class EpistemicPragmaticEngine:
    @staticmethod
    def _descriptor_values(entity: OntologyEntity, supplied: dict[str, float] | None) -> dict[str, float]:
        defaults = {descriptor.id: descriptor.default_value for descriptor in entity.descriptors}
        if supplied is None:
            return defaults
        unknown = set(supplied) - set(defaults)
        if unknown:
            raise ValueError(f"Unknown descriptors in request: {sorted(unknown)}")
        return {**defaults, **supplied}

    def relevance(
        self,
        request: RelevanceRequest,
        entity: OntologyEntity,
        policy: WeightingPolicy,
    ) -> RelevanceResponse:
        values = self._descriptor_values(entity, request.descriptor_values)
        descriptor_by_id = {descriptor.id: descriptor for descriptor in entity.descriptors}
        inputs = [
            WeightedInput(descriptor_id=descriptor_id, value=values[descriptor_id], weight=weight)
            for descriptor_id, weight in policy.weights.items()
        ]
        result = aggregate(request.aggregator, inputs, request.interaction_rules)
        denominator = result.raw_score if result.raw_score else 0.0
        contributions = [
            Contribution(
                descriptor_id=item.descriptor_id,
                label=descriptor_by_id[item.descriptor_id].label,
                value=item.value,
                weight=item.weight,
                weighted_contribution=round(item.weight * item.value, 6),
                normalized_contribution=round((item.weight * item.value) / denominator, 6) if denominator else 0.0,
            )
            for item in inputs
        ]
        contributions.sort(key=lambda item: item.weighted_contribution, reverse=True)

        warnings = [
            "The score expresses contextual relevance under the selected policy; it is not an ontological truth claim."
        ]
        if not policy.provenance.empirically_validated:
            warnings.append("The selected policy is illustrative or not yet empirically validated.")
        if request.aggregator == "weighted_sum":
            warnings.append(
                "The linear weighted sum assumes sufficiently comparable and approximately separable descriptor contributions."
            )

        return RelevanceResponse(
            ontology_id=entity.ontology_id,
            entity_id=entity.entity_id,
            policy_id=policy.policy_id,
            score=round(result.normalized_score, 6),
            raw_score=round(result.raw_score, 6),
            aggregator=request.aggregator,
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
        descriptor_by_id = {descriptor.id: descriptor for descriptor in entity.descriptors}
        required = set(descriptor_by_id)
        missing_left = required - set(request.left_values)
        missing_right = required - set(request.right_values)
        unknown = (set(request.left_values) | set(request.right_values)) - required
        if missing_left or missing_right or unknown:
            raise ValueError(
                "Similarity records must use the complete ontology-grounded descriptor schema. "
                f"MissingLeft={sorted(missing_left)} MissingRight={sorted(missing_right)} Unknown={sorted(unknown)}"
            )

        inputs: list[WeightedInput] = []
        rows: list[tuple[str, float, float]] = []
        for descriptor_id, weight in policy.weights.items():
            spec = request.comparators.get(descriptor_id, ComparatorSpec())
            similarity = compare(
                request.left_values[descriptor_id],
                request.right_values[descriptor_id],
                spec,
            )
            inputs.append(WeightedInput(descriptor_id=descriptor_id, value=similarity, weight=weight))
            rows.append((descriptor_id, similarity, weight))

        result = aggregate(request.aggregator, inputs, request.interaction_rules)
        denominator = result.raw_score if result.raw_score else 0.0
        contributions = [
            SimilarityContribution(
                descriptor_id=descriptor_id,
                label=descriptor_by_id[descriptor_id].label,
                left_value=request.left_values[descriptor_id],
                right_value=request.right_values[descriptor_id],
                similarity=round(similarity, 6),
                weight=weight,
                weighted_contribution=round(weight * similarity, 6),
                normalized_contribution=round((weight * similarity) / denominator, 6) if denominator else 0.0,
            )
            for descriptor_id, similarity, weight in rows
        ]
        contributions.sort(key=lambda item: item.weighted_contribution, reverse=True)

        warnings = [
            "Thresholded pairwise similarity supports an operational continuity decision, not numerical identity.",
            "The resulting continuity relation is not guaranteed to be transitive across a sequence of states.",
            "Longitudinal identity management should add lineage, provenance, or global continuity constraints.",
        ]
        if not policy.provenance.empirically_validated:
            warnings.append("The selected policy is illustrative or not yet empirically validated.")

        return SimilarityResponse(
            ontology_id=entity.ontology_id,
            entity_id=entity.entity_id,
            policy_id=policy.policy_id,
            left_record_id=request.left_record_id,
            right_record_id=request.right_record_id,
            score=round(result.normalized_score, 6),
            raw_score=round(result.raw_score, 6),
            threshold=request.threshold,
            operational_continuity_supported=result.normalized_score >= request.threshold,
            aggregator=request.aggregator,
            contributions=contributions,
            agent=policy.agent,
            context=policy.context,
            provenance=policy.provenance,
            applied_rules=result.applied_rules,
            warnings=warnings,
        )
