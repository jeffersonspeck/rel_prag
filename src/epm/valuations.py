"""Domain-specific valuation functions used to obtain v_I(p_i)."""

from __future__ import annotations

from typing import Any

from .models import ValuationSpec


def valuate(observed: Any, spec: ValuationSpec) -> float:
    """Convert a raw observation into the comparable unit interval."""
    if spec.kind == "categorical":
        key = str(observed)
        if key not in spec.categories:
            raise ValueError(f"Unknown categorical value '{key}'. Expected one of {sorted(spec.categories)}.")
        return spec.categories[key]

    try:
        number = float(observed)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Expected a numeric observation, received {observed!r}.") from exc

    if spec.kind == "normalized":
        if not 0.0 <= number <= 1.0:
            raise ValueError(f"Normalized observations must be in [0,1], received {number}.")
        return number

    assert spec.minimum is not None and spec.maximum is not None
    if not spec.minimum <= number <= spec.maximum:
        raise ValueError(
            f"Observation {number} is outside the declared range [{spec.minimum},{spec.maximum}]."
        )
    return (number - spec.minimum) / (spec.maximum - spec.minimum)
