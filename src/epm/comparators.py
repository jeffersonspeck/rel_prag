"""Descriptor-specific comparison functions s_i from article Equation 8."""

from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from .models import ComparatorSpec


def exact(left: Any, right: Any) -> float:
    # A discrete s_i: 1 when both values are equal, otherwise 0.
    return 1.0 if left == right else 0.0


def numeric_closeness(left: Any, right: Any, minimum: float, maximum: float) -> float:
    left_number = float(left)
    right_number = float(right)
    if not minimum <= left_number <= maximum or not minimum <= right_number <= maximum:
        raise ValueError(
            f"Numeric comparison values must stay within [{minimum},{maximum}]; "
            f"received {left_number} and {right_number}."
        )
    span = maximum - minimum
    distance = abs(left_number - right_number)
    # s_i(x,y) = max(0, 1 - |x-y| / (maximum-minimum)).
    return max(0.0, min(1.0, 1.0 - (distance / span)))


def string_ratio(left: Any, right: Any) -> float:
    return SequenceMatcher(None, str(left).casefold(), str(right).casefold()).ratio()


def jaccard(left: Any, right: Any) -> float:
    left_set = set(left if isinstance(left, (list, set, tuple)) else [left])
    right_set = set(right if isinstance(right, (list, set, tuple)) else [right])
    union = left_set | right_set
    if not union:
        return 1.0
    # s_i(X,Y) = |X intersection Y| / |X union Y|.
    return len(left_set & right_set) / len(union)


def compare(left: Any, right: Any, spec: ComparatorSpec) -> float:
    if spec.kind == "exact":
        return exact(left, right)
    if spec.kind == "numeric_closeness":
        assert spec.minimum is not None and spec.maximum is not None
        return numeric_closeness(left, right, spec.minimum, spec.maximum)
    if spec.kind == "string_ratio":
        return string_ratio(left, right)
    if spec.kind == "jaccard":
        return jaccard(left, right)
    raise ValueError(f"Unsupported comparator: {spec.kind}")
