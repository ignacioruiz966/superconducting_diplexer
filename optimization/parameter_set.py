from typing import Dict, Iterator, List, Union
import numpy as np

from parameter import Parameter

class ParameterSet:

    def __init__(self, parameters: List[Parameter]) -> None:
        names = [p.name for p in parameters]
        if len(names) != len(set(names)):
            raise ValueError(f"Duplicate parameter names detected.")
        
        self.parameters: Dict[str, Parameter] = {p.name: p for p in parameters}

    def __getitem__(self,name: str) -> Parameter:
        if name not in self.parameters:
            raise KeyError(f"Parameter '{name}' is not found in ParameterSet.")
        return self.parameters[name]

    def __iter__(self) -> Iterator[Parameter]:
        return iter(self.parameters.values())

    @property
    def design_values(self) -> Dict[str, float]:
        return {name: p.value for name, p in self.parameters.items()}

    @property
    def active_parameters(self) -> List[Parameter]:
        return [p for p in self.parameters.values() if not p.is_fixed]

    def get_design_vector(self) -> np.ndarray:
        return np.array([p.value for p in self.active_parameters], dtype=float)

    def set_design_vector(self, vector: Union[np.ndarray, list]) -> None:
        active = self.active_parameters
        if len(vector) != len(active):
            raise ValueError(f"Vector length({len(vector)} must match active parameters ({len(active)}).)")

        for param, val in zip(active, vector):
            param.set_value(val)

    def get_bounds_vector(self) -> List[tuple[float, float]]:
        bounds =[]
        for p in self.active_parameters:
            if p.bounds is None:
                raise ValueError(f"Active parameter '{p.name}' must have bounds defined for optimization.")
            bounds.append(p.bounds)
        return bounds

    def to_dict(self) -> Dict[str, dict]:
        return {
            name: {
                "value": p.value,
                "bounds": p.bounds,
                "is_fixed": p.is_fixed,
                "units": p.units
            }
            for name, p in self.parameters.items()
        }

    def __len__(self) -> int:
        return len(self.parameters)

    def __contains__(self, name: str) -> bool:
        return name in self.parameters

    def copy(self) -> "ParameterSet":
        copied_params = [
            Parameter(name=p.name, value=p.value, bounds=p.bounds) for p in self.parameters.values()
        ]
        return ParameterSet(copied_params)

    def keys(self):
        return self.parameters.keys()

    