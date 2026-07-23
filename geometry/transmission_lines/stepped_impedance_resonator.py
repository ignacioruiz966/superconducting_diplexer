import math

from geometry.geometry import Geometry
from typing import Tuple, List, Dict, Any
import gdsfactory as gf
from geometry.ports.ports import Port
from geometry.transmission_lines.stepped_impedance_section import SteppedImpedanceSection


class SteppedImpedanceResonator(Geometry):

    def __init__(self, start: Tuple[float, float], section_specs: List[Tuple[float, float]], orientation: float,
                 layer: str):
        self.start = start
        self.section_specs = section_specs
        self.orientation = orientation
        self.layer = layer

    def evaluate_composition(self) -> List[SteppedImpedanceSection]:
        sections = []
        current_origin = self.start
        for width, length in self.section_specs:
            sec = SteppedImpedanceSection(current_origin, width, length, self.orientation, self.layer)
            sections.append(sec)
            current_origin = sec.ports["output"].center
        return sections

    @property
    def ports(self) -> dict[str, Port]:
        evaluated = self.evaluate_composition()
        if not evaluated: return {}
        return {
            "input": evaluated[0].ports["input"],
            "output": evaluated[-1].ports["output"]
        }

    @property
    def polygons(self):
        sect = self.evaluate_composition()
        poly = []
        for s in sect:
            poly.append(s.polygons)
        return poly

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'SteppedImpedanceResonator':

        geometry_type = config.get("type")

        if geometry_type != "stepped_impedance_resonator":
            raise TypeError(f"Invalid geometry type: '{geometry_type}'. Expected 'stepped_impedance_resonator'")


        if not isinstance(config, dict):
            raise TypeError("The configuration must be a dictionary")

        layer = config.get("layer")
        orientation = config.get("orientation")
        origin = config.get("origin")
        sections = config.get("sections")

        if layer is None or orientation is None or sections is None or origin is None:
            raise ValueError(
                "Configuration missing required fields: 'layer', 'orientation', 'origin', 'sections'"
            )

        start = (origin[0], origin[1])
        orientation = float(orientation)
        specs = [(s["width"],s["length"]) for s in sections]

        return cls(
            start=start,
            section_specs=specs,
            orientation=orientation,
            layer=layer,
        )

    def translate(self, dx: float, dy: float) -> 'Geometry':
        new_start = (self.start[0] + dx, self.start[1] + dy)
        return SteppedImpedanceResonator(new_start, self.section_specs, self.orientation, self.layer)

    def rotate(self, angle: float, origin: Tuple[float, float] = (0.0, 0.0)) -> "Geometry":
        ox, oy = origin
        dx, dy = self.start[0] - ox, self.start[1] - oy
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        rx = ox + (dx * cos_a - dy * sin_a)
        ry = oy + (dx * sin_a - dy * cos_a)
        return SteppedImpedanceResonator((rx, ry), self.section_specs, self.orientation, self.layer)

    def build(self) -> "Any":
        sect = self.evaluate_composition()

        component = gf.Component()

        for s in sect:
            geometry = s.build()
            component << geometry
        return component


    def validate(self) -> None:
        pass

    def describe(self) -> str:
        pass

