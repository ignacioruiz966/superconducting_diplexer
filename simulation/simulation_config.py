from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class SimulationConfig:
    """
    Represents electromagnetic simulation settings.
    This model remains independent of any specific
    vendor (like sonnet) syntax or execution.
    """

    start_frequency: float
    stop_frequency: float
    frequency_points: int
    box_width: float
    box_height: float
    ports: int
    output: dict

    def __post_init__(self) -> None:

        if self.start_frequency <= 0:
            raise ValueError(f"start_frequency must be greater than 0, got {self.start_frequency}")

        if self.stop_frequency <= self.start_frequency:
            raise ValueError(f"Stop frequency ({self.stop_frequency}) must be greater than start frequency ({self.stop_frequency})")

        if self.frequency_points < 2:
            raise ValueError(f"Must have at least 2 frequency points, got {self.frequency_points}")

        if self.box_width <= 0 or self.box_height <= 0:
            raise ValueError(f"Box dimensions must be positive, got ({self.box_width}, {self.box_height})")

        if self.ports < 2:
            raise ValueError(f"Must have at least 2 ports, got {self.ports}")

        if self.output is None:
            raise ValueError("Output is empty")

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'SimulationConfig':

        return cls(
            start_frequency=float(config["start_frequency"]),
            stop_frequency=float(config["stop_frequency"]),
            frequency_points=int(config["frequency_points"]),
            box_width=float(config["box_width"]),
            box_height=float(config["box_height"]),
            ports=int(config["ports"]),
            output=config["output_sonnet"],
        )

