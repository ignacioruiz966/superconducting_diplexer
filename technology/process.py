from dataclasses import dataclass

@dataclass(frozen=True)
class Process:

    """
    Represents the fabrication process used to
    manufacture superconducting geometry devices,
    including material definitions and GDS layer mappings.
    """

    substrate: str
    conductor: str
    dielectric: str
    ground: str

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
            if not isinstance(value, dict):
                raise ValueError(f"Material {field_name} is not a dictionary")


    @classmethod
    def from_config(cls, config: dict) -> "Process":

        process_data = config

        if not isinstance(process_data, dict):
            raise ValueError("Configuration dictionary is missing the required 'process' section")

        required_fields = ["substrate", "conductor",
                           "dielectric", "ground",
                           ]

        extracted_kwargs = {}
        for field in required_fields:
            if field not in process_data:
                raise ValueError(f"Field {field} is missing")
            extracted_kwargs[field] = process_data[field]

        return cls(**extracted_kwargs)
