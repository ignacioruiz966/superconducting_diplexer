class SonnetExporter:
    def __init__(self):
        pass

    @staticmethod
    def export_geometry(project, geometry):
        for poly in geometry:
            project.add_polygons("metal", poly, tech_layer="TiN")
