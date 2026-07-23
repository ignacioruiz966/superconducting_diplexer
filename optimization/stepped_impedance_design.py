from parameterized_design import ParameterizedDesign
from parameter_set import ParameterSet
from typing import Dict, Any


class SteppedImpedanceDesign(ParameterizedDesign):

    def __init__(self, parameters: ParameterSet):
        super().__init__(parameters)

    def build_config(self) -> Dict[str, Any]:
        sections = []
        width_keys = sorted([k for k in self.parameters.keys() if k.startswith("W")])


        for w_key in width_keys:
            i = w_key[1:]
            sections.append({
                "width": self.parameters[w_key].value,
                "length": self.parameters[f"L{i}"].value,
            })

        return {
            "type": "stepped_impedance_resonator",
            "layer": "TiN",
            "orientation": 0,
            "origin": [0, 0],

            "sections": sections
        }