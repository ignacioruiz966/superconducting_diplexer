from abc import ABC, abstractmethod
from typing import Any, Dict
from parameter_set import ParameterSet


class ParameterizedDesign(ABC):

    def __init__(self, parameters: ParameterSet):
        self.parameters = parameters


    @abstractmethod
    def build_config(self) -> Dict[str, Any]:
        pass