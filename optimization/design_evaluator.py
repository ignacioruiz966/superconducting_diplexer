from simulation.simulation_config import SimulationConfig
from simulation.sonnet.project import SonnetProject
from simulation.sonnet.results import SonnetResults
from simulation.sonnet.runner import SonnetRunner
from geometry.geometry_factory import GeometryFactory
from parameterized_design import ParameterizedDesign
from technology.process import Process
from typing import Tuple, Dict


class DesignEvaluator:

    def __init__(
            self,
            factory: GeometryFactory,
            process: Process,
            simulation_config: SimulationConfig,
            runner: SonnetRunner,
            cached_enabled: bool = True,
    ):

        self.factory = factory
        self.process = process
        self.simulation_config = simulation_config
        self.runner = runner
        self.cached_enabled = cached_enabled
        self.cache: Dict[Tuple[float, float], SonnetResults] = {}


    def evaluate(self, design: ParameterizedDesign):
        key = self.cache_key(design)
        if self.cached_enabled and key in self.cache:
            return self.cache[key]

        config = design.build_config()

        geometry = self.factory.create(config)

        project = SonnetProject(self.process, self.simulation_config, geometry)
        project.setup_simulation()

        s2p_path = self.runner.run_simulation()

        results = SonnetResults(s2p_path)

        if self.cached_enabled:
            self.cache[key] = results

        return results

    @staticmethod
    def cache_key(self, design: ParameterizedDesign) -> Tuple[float, ...]:
        return tuple(design.parameters.get_design_vector())
    
    def clear_cache(self) -> None:
        self.cache.clear()

    @property
    def cache_size(self) -> int:
        return len(self.cache)


