from dataclasses import dataclass, field
from typing import Dict, Any
from functools import cached_property


@dataclass(frozen=True)
class DesignConfig:
    """Immutable representation of a
    parsed CAD design configuration."""

    raw_config: Dict[str, Any] = field(repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.raw_config, dict):
            raise TypeError("Configuration file must be a dict")

        required_sections = {'design', 'geometry', 'process', 'output'}
        missing_sections = required_sections - self.raw_config.keys()

        if missing_sections:
            raise ValueError(f"The following sections are missing: {missing_sections}")


    @cached_property
    def design(self) -> Dict[str, Any]:
        return self.raw_config['design']

    @cached_property
    def geometry(self) -> Dict[str, Any]:
        return self.raw_config['geometry']

    @cached_property
    def process(self) -> Dict[str, Any]:
        return self.raw_config['process']

    @cached_property
    def output(self) -> Dict[str, Any]:
        return self.raw_config['output']
