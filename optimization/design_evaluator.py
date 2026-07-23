from simulation.sonnet.exporter import SonnetExporter
from simulation.sonnet.runner import SonnetRunner
from geometry.geometry_factory import GeometryFactory
from parameterized_design import ParameterizedDesign


class DesignEvaluator:

    def __init__(self, factory: GeometryFactory, exporter: SonnetExporter, runner: SonnetRunner):
        self.factory = factory
        self.exporter = exporter
        self.runner = runner

    def evaluate(self, design: ParameterizedDesign):
        config = design.build_config()

        geometry = self.factory.create(config)

        project = self.exporter.export_geometry(geometry)

        results = self.runner.run_simulation()

        return results


