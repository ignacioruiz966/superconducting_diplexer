from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any

from geometry.ports.ports import Port
from geometry.polygon import Polygon
from technology.process import Process
import numpy as np

class Geometry(ABC):

    """
    Abstract Base Class defining the contract
    for all geometry geometries.
    """

    @property
    @abstractmethod
    def ports(self) -> dict[str, Port]:
        ...

    @classmethod
    @abstractmethod
    def from_config(cls, config: Dict[str, Any]) -> 'Geometry':
        ...

    @abstractmethod
    def translate(self, dx: float, dy: float) -> 'Geometry':
        ...

    @abstractmethod
    def rotate(self, angle: float, origin: Tuple[float, float] =  (0.0, 0.0)) -> "Geometry":
        ...

    @abstractmethod
    def build(self) -> "Any":
        ...

    @abstractmethod
    def validate(self) -> None:
        ...

    @abstractmethod
    def describe(self) -> str:
        ...

    @property
    @abstractmethod
    def polygons(self) -> List[np.ndarray]:
        ...
