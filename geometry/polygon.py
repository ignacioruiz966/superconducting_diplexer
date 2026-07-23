from dataclasses import dataclass, field, replace
from typing import Tuple
import math
from typing import Dict, List, Any


@dataclass(frozen=True)
class Polygon:

    points: List[Tuple[float, float]]
    layer: str
    purpose: str = "main"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def translate(self, dx: float, dy: float) -> "Polygon":
        return replace(self, points=[ (p[0] + dx, p[1] + dy) for p in self.points])

    def rotate(self, angle: float, origin: Tuple[float, float] = (0.0, 0.0)) -> "Polygon":
        ox, oy = origin
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        new_points = []
        for px, py in self.points:
            dx, dy = px - ox, py - oy
            rx = ox + (dx * cos_a - dy * sin_a)
            ry = oy + (dx * sin_a + dy * cos_a)
            new_points.append((rx, ry))
        return replace(self, points=new_points)

