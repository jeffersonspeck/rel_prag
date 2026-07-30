"""Aggregation strategies for Agg_C.

The weighted average is the default normalized baseline. The weighted sum is
kept for direct correspondence with the paper's illustrative equation. The
rule-aware strategy demonstrates that interactions, requirements, and vetoes
can be represented without redefining the ontology.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Iterable

from .exceptions import AggregationError
from .models import InteractionRule


@dataclass(frozen=True)
class WeightedInput:
    descriptor_id: str
    value: float
    weight: float


@dataclass(frozen=True)
class AggregationResult:
    raw_score: float
    score: float
    normalized: bool
    applied_rules: list[str]


def _validate(inputs: list[WeightedInput]) -> None:
    if not inputs:
        raise AggregationError("Aggregation requires at least one descriptor.")
    if any(item.weight < 0.0 for item in inputs):
        raise AggregationError("Weights cannot be negative.")
    if any(not 0.0 <= item.value <= 1.0 for item in inputs):
        raise AggregationError("All aggregation values must be in the [0,1] interval.")


def weighted_sum(inputs: Iterable[WeightedInput]) -> AggregationResult:
    items = list(inputs)
    _validate(items)
    raw = sum(item.weight * item.value for item in items)
    weight_total = sum(item.weight for item in items)
    # The paper's linear equation is a raw sum. It is comparable on [0,1] only
    # when the policy explicitly normalizes its weights.
    return AggregationResult(
        raw_score=raw,
        score=raw,
        normalized=isclose(weight_total, 1.0, abs_tol=1e-9),
        applied_rules=[],
    )


def weighted_average(inputs: Iterable[WeightedInput]) -> AggregationResult:
    items = list(inputs)
    _validate(items)
    raw = sum(item.weight * item.value for item in items)
    weight_total = sum(item.weight for item in items)
    normalized = raw / weight_total if weight_total else 0.0
    return AggregationResult(
        raw_score=raw,
        score=normalized,
        normalized=True,
        applied_rules=[],
    )


def rule_aware(inputs: Iterable[WeightedInput], rules: list[InteractionRule]) -> AggregationResult:
    items = list(inputs)
    baseline = weighted_average(items)
    by_id = {item.descriptor_id: item for item in items}
    score = baseline.score
    applied: list[str] = []

    for rule in rules:
        selected = [by_id[descriptor_id] for descriptor_id in rule.descriptors if descriptor_id in by_id]
        if len(selected) != len(rule.descriptors):
            missing = sorted(set(rule.descriptors) - set(by_id))
            raise AggregationError(f"Rule '{rule.rule_id}' references unknown descriptors: {missing}")

        values = [item.value for item in selected]
        if rule.kind == "synergy" and all(value >= rule.trigger for value in values):
            score += rule.coefficient * min(values)
            applied.append(f"{rule.rule_id}:synergy")
        elif rule.kind == "redundancy" and all(value >= rule.trigger for value in values):
            score -= rule.coefficient * min(values)
            applied.append(f"{rule.rule_id}:redundancy")
        elif rule.kind == "veto" and any(value < rule.trigger for value in values):
            score = 0.0
            applied.append(f"{rule.rule_id}:veto")
        elif rule.kind == "requirement" and not all(value >= rule.trigger for value in values):
            score = 0.0
            applied.append(f"{rule.rule_id}:requirement-not-met")

    return AggregationResult(
        raw_score=baseline.raw_score,
        score=max(0.0, min(1.0, score)),
        normalized=True,
        applied_rules=applied,
    )


def aggregate(
    strategy: str,
    inputs: Iterable[WeightedInput],
    rules: list[InteractionRule] | None = None,
) -> AggregationResult:
    if strategy == "weighted_sum":
        return weighted_sum(inputs)
    if strategy == "weighted_average":
        return weighted_average(inputs)
    if strategy == "rule_aware":
        return rule_aware(inputs, rules or [])
    raise AggregationError(f"Unknown aggregation strategy: {strategy}")
