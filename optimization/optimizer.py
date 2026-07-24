from abc import ABC, abstractmethod
from typing import List, Optional

from scipy.optimize import differential_evolution, minimize

from .callback import Callback, CallbackList
from .history import OptimizationHistory
from .objective import ObjectiveFunction
from .parameterized_design import ParameterizedDesign


class Optimizer(ABC):

    def __init__(self, callbacks: Optional[List[Callback]] = None):
        self.callbacks = CallbackList(callbacks or [])
        self.history = OptimizationHistory()
        self.iteration = 0

    @abstractmethod
    def optimize(self, objective_function: ObjectiveFunction, design: ParameterizedDesign):
        ...

    def tracked(self, objective_function: ObjectiveFunction, design: ParameterizedDesign):

        def wrapped(vector):
            self.history.start_iteration()
            score = objective_function(vector)
            self.iteration += 1
            self.history.record(self.iteration, design.parameters, score)
            self.callbacks.on_iteration(self.iteration, design.parameters, score)
            return score

        return wrapped


class DifferentialEvolutionOptimizer(Optimizer):

    def __init__(self, callbacks: Optional[List[Callback]] = None, **scipy_kwargs):
        super().__init__(callbacks)
        self.scipy_kwargs = scipy_kwargs

    def optimize(self, objective_function: ObjectiveFunction, design: ParameterizedDesign):
        bounds = design.parameters.get_bounds_vector()
        self.callbacks.on_start()

        result = differential_evolution(
            self.tracked(objective_function, design),
            bounds=bounds,
            **self.scipy_kwargs
        )

        design.parameters.set_design_vector(result.x)
        self.callbacks.on_end(results=result)
        return result

class NelderMeadOptimizer(Optimizer):

    def __init__(self, callbacks: Optional[List[Callback]] = None, **scipy_kwargs):
        super().__init__(callbacks)
        self.scipy_kwargs = scipy_kwargs

    def optimize(self, objective_function: ObjectiveFunction, design: ParameterizedDesign):
        x0 = design.parameters.get_bounds_vector()
        self.callbacks.on_start()

        result = minimize(
            self.tracked(objective_function, design),
            x0=x0,
            method="Nelder-Mead",
            **self.scipy_kwargs
        )

        design.parameters.set_design_vector(result.x)
        self.callbacks.on_end(results=result)
        return result
