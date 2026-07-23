from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Parameter:

    name: str
    value: float
    bounds: Optional[tuple[float, float]] = None
    is_fixed: bool = False
    units: str = "um"
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.bounds:
            lower, upper = self.bounds
            if lower > upper:
                raise ValueError("Lower bound must be less than upper bound")
            if not (lower <= self.value <= upper):
                raise ValueError(
                    f"Initial value {self.value} is outside the bounds"
                    f"({lower}, {upper} for '{self.name}')."
                )

    def set_value(self, new_value: float):
        if self.is_fixed:
            return

        if self.bounds:
            lower, upper = self.bounds
            if not (lower <= new_value <= upper):
                raise ValueError(
                    f"Value{new_value} out of bounds for '{self.name}' ({lower} to {upper} {self.units})."
                )
        self.value = new_value

    @property
    def lower_bound(self) -> Optional[float]:
        return self.bounds[0] if self.bounds else None

    @property
    def upper_bound(self) -> Optional[float]:
        return self.bounds[1] if self.bounds else None

    @property
    def normalized_value(self) -> float:
        if self.bounds is None:
            raise ValueError(f"Cannot normalize parameter '{self.name}' without bounds.")
        lower, upper = self.bounds
        return (self.value - lower) / (upper - lower)

    def from_normalized(self, normalized_x: float) -> float:
        if self.bounds is None:
            raise ValueError(f"Cannot denormalize parameter '{self.name}' without bounds.")
        lower, upper = self.bounds
        return lower + (normalized_x * (upper - lower))

    def __str__(self) -> str:
        return f"{self.name} = {self.value:.4f} {self.units}"

