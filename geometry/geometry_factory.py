from typing import Any, Dict

from geometry.transmission_lines.stepped_impedance_resonator import SteppedImpedanceResonator
from technology.process import Process
from geometry.inverted_microstrip import InvertedMicrostrip

class GeometryFactory:
    """
    Factory to instantiate geometry objects
    without coupling the main pipeline
    """
    @staticmethod
    def create(geometry_config: Dict[str, Any]) -> Any:

        geometry_type = geometry_config.get("type")
        if not geometry_type:
            raise ValueError("Geometry configuration is missing the required 'type' key")

        supported_types = {
            "inverted_microstrip": InvertedMicrostrip,
            "stepped_impedance_resonator": SteppedImpedanceResonator,
        }

        if geometry_type not in supported_types:
            supported_list = ",".join(f"'{t}'" for t in supported_types.keys())
            raise ValueError(
                f"Unsupported geometry type: {geometry_type}. "
                f"Supported types are: {supported_list}."
            )

        geometry_class = supported_types[str(geometry_type)]

        return geometry_class.from_config(geometry_config)