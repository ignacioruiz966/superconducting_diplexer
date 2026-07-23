from distutils.command.config import config

import pysonnet as ps
from geometry.geometry import Geometry
from simulation.simulation_config import SimulationConfig
from technology.process import Process
from simulation.sonnet.exporter import SonnetExporter
from pathlib import Path

class SonnetProject:

    def __init__(self, process: Process, config: SimulationConfig, geometry: Geometry) -> None:
        self.process = process
        self.config = config
        self.geometry = geometry

    def setup_simulation(self):

        start_frequency = self.config.start_frequency
        stop_frequency = self.config.stop_frequency
        box_x = self.config.box_width
        box_y = self.config.box_height
        conductor = self.process.conductor
        ground = self.process.ground
        substrate = self.process.substrate
        dielectric = self.process.dielectric

        project = ps.GeometryProject()

        project['control']['res_detection'] = False

        project.set_units(length='um')

        project.setup_box(box_x, box_y, 400, 200)

        project.define_metal("general", conductor["name"], ls=12, thickness=conductor["thickness"])
        project.define_metal("general", ground["name"], ls=0.1, thickness=ground["thickness"])

        project.set_box_cover("free space", top=True)
        project.set_box_cover("free space", bottom=True)

        project.add_dielectric("Air", 0, thickness=1000)
        project.add_dielectric(dielectric["name"], dielectric["layer"], thickness=dielectric["thickness"],
                               epsilon=dielectric["er"], dielectric_loss=1.0e-5,)
        project.add_dielectric(substrate["name"], substrate["layer"], thickness=substrate["thickness"],
                               epsilon=substrate["er"])


        project.define_technology_layer("metal", ground["name"],
                                        ground["layer"], ground["name"])
        project.define_technology_layer("metal", "TiN",
                                        conductor["layer"], conductor["name"])

        project.add_frequency_sweep("abs", f1=start_frequency, f2=stop_frequency)
        project.set_analysis("frequency sweep")

        exporter = SonnetExporter()
        self.geometry = self.geometry.translate(0, box_y/2)
        exporter.export_geometry(project, self.geometry.polygons, box_x, box_y)

        ports = self.geometry.ports

        port1 = ports.get("input")
        port2 = ports.get("output")

        project.add_port("standard", 1,port1.x, port1.y, 50, level=conductor["layer"])
        project.add_port("standard", 2,port2.x,port2.y, 50, level=conductor["layer"])

        project.add_syz_parameter_file("touchstone")

        output_sonnet = self.config.output
        output_son = Path(output_sonnet.get("sonnet_directory"))

        son_filename = output_sonnet.get("son_filename", "testfile.son")

        sonnet_file_path = output_son / son_filename
        print(f"Writing simulation output to: {output_son}")
        project.make_sonnet_file(sonnet_file_path)



