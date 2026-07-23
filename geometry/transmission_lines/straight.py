import gdsfactory as gf
from typing import Dict
import math
import numpy as np

from geometry.geometry import Geometry
from geometry.polygon import Polygon
from geometry.ports.ports import Port
from typing import List, Tuple, Any


class Straight(Geometry):

    @property
    def polygons(self) -> List[np.ndarray]:
        x = self.start[0]
        y = self.start[1]

        return [
            np.array([
                [x, y - self.width / 2],
                [x + self.length, y - self.width / 2],
                [x + self.length, y +  self.width / 2],
                [x , y + self.width / 2],
            ])
        ]


    def rotate(self, angle: float, origin: Tuple[float, float] = (0.0, 0.0)) -> "Straight":
        ox, oy = origin
        dx, dy = self.start[0] - ox, self.start[1] - oy
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        rx = ox + (dx * cos_a - dy * sin_a)
        ry = oy + (dx * sin_a + dy * cos_a)
        return Straight((rx, ry), self.width, self.length, self.orientation, self.layer)


    def __init__(self, start: Tuple[float, float], width: float, length: float, orientation: float, layer: str) -> None:
        self.start = start
        self.width = width
        self.length = length
        self.orientation = orientation
        self.layer = layer


    @property
    def ports(self) -> dict[str, Port]:
        dx = self.length * math.cos(self.orientation)
        dy = self.length * math.sin(self.orientation)
        end = (self.start[0] + dx, self.start[1] + dy)
        return {
            "input": Port("input", self.start, self.orientation + math.pi, self.width, self.layer),
            "output": Port("output", end, self.orientation, self.width, self.layer),
        }

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'Geometry':
        pass

    def translate(self, dx: float, dy: float) -> "Straight":
        new_start = (self.start[0] + dx, self.start[1] + dy)
        return Straight(new_start, self.width, self.length, self.orientation, self.layer)

    def build(self) -> "Any":

        component = gf.Component()
        straight = gf.components.straight(length=self.length, width=self.width)
        ref = component << straight
        ref.move(self.start)
        return component




    def validate(self) -> None:
        pass

    def describe(self) -> str:
        pass
