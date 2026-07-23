from dataclasses import dataclass, field, replace

import math


@dataclass(frozen=True)
class Port:
    """
    Represents a geometry connection point.
    """

    name: str
    center: tuple[float, float]
    orientation: float
    width: float
    layer: str

    def __post_init__(self):
        normalized_angle = self.orientation % (2 * math.pi)
        object.__setattr__(self, 'orientation', normalized_angle)

    @property
    def x(self) -> float:
        return self.center[0]

    @property
    def y(self) -> float:
        return self.center[1]

    def translate(self, dx: float, dy: float) -> "Port":
        new_center = (self.center[0] + dx, self.center[1] + dy)
        return replace(self, center=new_center)

    def rotate(self, angle: float, origin: tuple[float, float]) -> "Port":

        ox,oy = origin
        dx = self.x - ox
        dy = self.y - oy

        cos_a, sin_a = math.cos(angle), math.sin(angle)
        rx = ox + (dx * cos_a - dy * sin_a)
        ry = oy + (dx * sin_a + dy * cos_a)

        new_orientation = (self.orientation + angle) % (2 * math.pi)
        return replace(self, center=(rx,ry), orientation=new_orientation)

    def connect_verify(self, other: "Port") -> "bool":

        angle_diff = abs((self.orientation - other.orientation) % (2 * math.pi))
        opposite = math.isclose(angle_diff, math.pi, abs_tol=1e-5)

        coincident = math.isclose(self.x, other.x, abs_tol=1e-5) and math.isclose(self.y, other.y, abs_tol=1e-5)

        return all([
            math.isclose(self.width, other.width, abs_tol=1e-5),
            self.layer == other.layer,
            opposite,
            coincident,
        ])


