from dataclasses import dataclass

from networkx.utils import random_sequence


@dataclass(frozen=True)
class Process:
    """Represents the fabrication process used to
    manufacture superconducting microwave devices,
    including material definitions and GDS layer mappings."""

    substrate: str
    conductor: str
    dielectric: str
    ground: str
    conductor_layer: tuple[int, int]

    def __post_init__(self):

        # Prevent empty or blank string inputs
        materials = {
            "Substrate": self.substrate,
            "Conductor": self.conductor,
            "Dielectric": self.dielectric,
            "Ground": self.ground,
        }

        for field_name, value in materials.items():
            if value is None:
                raise ValueError(f"Material {field_name} cannot be None")
            if not isinstance(value, str):
                raise ValueError(f"Material {field_name} is not a string")
            if not value.strip():
                raise ValueError(f"Material {field_name} is empty")

        # Verify layer values make sense (e.g., non-negative layer numbers)
        if self.conductor_layer is None:
            raise ValueError("Layer cannot be None")
        if not isinstance(self.conductor_layer, tuple):
            raise ValueError(f"Layer {self.conductor_layer} is not a tuple")
        if any(layer < 0 for layer in self.conductor_layer):
            raise ValueError("Conductor layer cannot be negative")


    @classmethod
    def from_config(cls, config: dict) -> "Process":

        process_data = config

        if not isinstance(process_data, dict):
            raise ValueError("Configuration dictionary is missing the required 'process' section")

        required_fields = ["substrate", "conductor",
                           "dielectric", "ground",
                           "conductor_layer"]

        extracted_kwargs = {}
        for field in required_fields:
            if field not in process_data:
                raise ValueError(f"Field {field} is missing")
            extracted_kwargs[field] = process_data[field]

        conductor_layer = extracted_kwargs["conductor_layer"]

        if isinstance(conductor_layer, list) and len(conductor_layer) == 2:
            extracted_kwargs["conductor_layer"] = tuple(conductor_layer)
        if not any(isinstance(layer, int) for layer in conductor_layer):
            raise ValueError("Conductor layer must be an integer")
        if not isinstance(extracted_kwargs["conductor_layer"], tuple):
            raise TypeError("conductor_layer must be a list of 2 integers or a tuple.")

        return cls(**extracted_kwargs)
