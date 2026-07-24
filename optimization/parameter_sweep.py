from itertools import product
from typing import Dict, Iterable, Sequence

from optimization.parameterized_design import ParameterizedDesign


class ParameterSweep:

    def __init__(self, design: ParameterizedDesign, values: Dict[str, Sequence[float]]):
        self.design = design
        self.values = values

        for name in values:
            if name not in design.parameters:
                raise KeyError(f"Parameter {name} not present in design's ParameterSet")

    def __iter__(self) -> Iterable[ParameterizedDesign]:
        names = list(self.values.keys())
        grids = [self.values[name] for name in names]
        design_cls = type(self.design)

        for combination in product(*grids):
            parameters = self.design.parameters.copy()
            parameters.update(dict(zip(names, combination)))
            yield design_cls(parameters)

    def __len__(self) -> int:
        total = 1
        for values in self.values.values():
            total *= len(values)
        return total
    