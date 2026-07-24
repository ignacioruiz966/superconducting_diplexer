from abc import ABC, abstractmethod
from typing import Iterable, Sequence
from parameter_set import ParameterSet


class Constraint(ABC):

    @abstractmethod
    def evaluate(self, parameters: ParameterSet) -> float:
        ...

    def is_satisfied(self, parameters: ParameterSet) -> bool:
        return self.evaluate(parameters) <= 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"


class MinLinewidth(Constraint):

    def __init__(self, parameter_name: str, minimum: float):
        self.parameter_name = parameter_name
        self.minimum = minimum

    def evaluate(self, parameters: ParameterSet) -> float:
        return self.minimum - parameters[self.parameter_name].value

    def __repr__(self) -> str:
        return f"MinLinewidth('{self.__class__.__name__}', minumum={self.minimum})"


class MinSpacing(Constraint):

    def __init__(self, parameter_a: str, parameter_b: str, minimum: float):
        self.parameter_a = parameter_a
        self.parameter_b = parameter_b
        self.minimum = minimum

    def evaluate(self, parameters: ParameterSet) -> float:
        gap = abs(parameters[self.parameter_a].value - parameters[self.parameter_b].value)
        return self.minimum - gap

    def __repr__(self) -> str:
        return f"MinSpacing('{self.parameter_a}', '{self.parameter_b}', minimum={self.minimum})"

class MaxLength(Constraint):

    def __init__(self, parameter_names: Sequence[str], maximum: float):
        self.parameter_names = list(parameter_names)
        self.maximum = maximum

    def evaluate(self, parameters: ParameterSet) -> float:
        total = sum(parameters[name].value for name in self.parameter_names)
        return total - self.maximum

    def __repr__(self) -> str:
        return f"MaxLength('{self.parameter_names}', maximum={self.maximum})"

class CompositeConstraint(Constraint):

    def __init__(self, constraints: Iterable[Constraint]):
        self.constraints = list(constraints)

    def evaluate(self, parameters: ParameterSet) -> float:
        if not self.constraints:
            return 0.0
        return max(c.evaluate(parameters) for c in self.constraints)

    def __repr__(self) -> str:
        return f"CompositeConstraint({self.constraints!r})"