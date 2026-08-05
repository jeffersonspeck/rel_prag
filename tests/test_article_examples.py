import pytest

from epm.aggregators import WeightedInput, weighted_sum


def test_equations_12_and_13_geographic_example():
    weights = [0.10, 0.35, 0.20, 0.10, 0.15, 0.10]
    similarities = [1.0, 0.8, 0.9, 0.7, 1.0, 0.8]
    result = weighted_sum(
        WeightedInput(descriptor_id=f"p_{index}", value=value, weight=weight)
        for index, (value, weight) in enumerate(zip(similarities, weights), start=1)
    )

    assert result.normalized is True
    assert result.score == pytest.approx(0.86)
    assert result.score >= 0.85  # Equation 13: contextual continuity is supported.
