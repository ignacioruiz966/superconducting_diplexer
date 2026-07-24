from abc import ABC, abstractmethod
from typing import Callable, Iterable, Optional
from constraint import Constraint
from metric import Bandwidth, InsertionLoss, LoadedQ, Metric, ResonantFrequency, ReturnLoss


class Objective(ABC):

    @abstractmethod
    def evaluate(self, results) -> float:
        ...

    def __call__(self, results) -> float:
        return self.evaluate(results)

    def __add__(self, other: "Objective") -> "Objective":
        return SumObjective(self, other)

    __radd__ = __add__

    def __sub__(self, other: "Objective") -> "Objective":
        return SumObjective(self, WeightedObjective(other, -1.0))

    def __mul__(self, weight: float) -> "Objective":
        return WeightedObjective(self, weight)

    __rmul__ = __mul__

    def __neg__(self) -> "Objective":
        return WeightedObjective(self, -1.0)


class SumObjective(Objective):

    def __init__(self, left: Objective, right: Objective):
        self.left = left
        self.right = right

    def evaluate(self, results) -> float:
        return self.left.evaluate(results) + self.right.evaluate(results)

    def __repr__(self) -> str:
        return f"({self.left!r} + {self.right!r})"


class WeightedObjective(Objective):

    def __init__(self, objective: Objective, weight: float):
        self.objective = objective
        self.weight = weight

    def evaluate(self, results) -> float:
        return self.weight * self.objective.evaluate(results)

    def __repr__(self) -> str:
        return f"{self.weight}*{self.objective!r}"


class MetricObjective(Objective):

    def __init__(
            self,
            metric: Metric,
            target: Optional[float] = None,
            penalty: Optional[Callable[[float, float], float]] = None,
    ):
        self.metric = metric
        self.target = target
        self.penalty = penalty

    def evaluate(self, results) -> float:
        value = self.metric.evaluate(results)
        if self.target is None:
            return value
        return self.penalty(value, self.target)

    def __repr__(self) -> str:
        return f"MetricObjective({self.metric!r}, target={self.target!r})"


class FrequencyObjective(MetricObjective):

    def __init__(self, target: float, penalty=None):
        super().__init__(ResonantFrequency(), target=target, penalty=penalty)


class InsertionLossObjective(MetricObjective):

    def __init__(self, target: float = 0.0, frequency: Optional[float] = None, penalty=None):
        super().__init__(InsertionLoss(frequency=frequency), target=target, frequency=frequency, penalty=penalty)


class ReturnLossObjective(MetricObjective):
    def __init__(self, target: float = -20.0, frequency: Optional[float] = None, penalty=None):
        super().__init__(ReturnLoss(frequency=frequency), target=target, penalty=penalty)


class LoadedQObjective(MetricObjective):

    def __init__(self, target: float, penalty=None):
        super().__init__(LoadedQ(), target=target, penalty=penalty)


class BandwidthObjective(MetricObjective):

    def __init__(self, target: float, frequency: Optional[float] = None, penalty=None):
        super().__init__(Bandwidth(), target=target, penalty=penalty)


class ObjectiveFunction:

    def __init__(
            self,
            evaluator,
            design,
            objective: Objective,
            constraints: Optional[Iterable[Constraint]] = None,
            penalty_value: float = 1e6,
    ):
        self.evaluator = evaluator
        self.design = design
        self.objective = objective
        self.constraints = list(constraints) if constraints else []
        self.penalty_value = penalty_value

    def __call__(self, vector) -> float:
        self.design.parameters.set_design_vector(vector)

        violation = self.max_constraint_violation()
        if violation > 0:
            return self.penalty_value + violation

        results = self.evaluator.evaluate(self.design)
        return self.objective.evaluate(results)

    def max_constraint_violation(self) -> float:
        if not self.constraints:
            return 0.0
        return max(c.evaluate(self.design.parameters) for c in self.constraints)

