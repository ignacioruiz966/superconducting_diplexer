from typing import Protocol

import numpy as np

class SonnetExporter:
    def __init__(self):
        pass

    @staticmethod
    def export_geometry(project, geometry, box_x, box_y):
        for poly in geometry:
            project.add_polygons("metal", poly, tech_layer="TiN")

        ground = [np.array([
                [0, 0],
                [0, box_y],
                [box_x, box_y],
                [box_x, 0],
        ])]
        project.add_polygons("metal", ground, tech_layer="Nb")
