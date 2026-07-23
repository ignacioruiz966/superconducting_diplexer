from pathlib import Path
class GdsExport:

    def __init__(self, config, geometry):
        self.geometry = geometry
        self.config = config


    def export(self):
        output_gds = self.config.get("gds")

        output_dir = Path(output_gds.get("gds_directory", "gds"))
        gds_filename = output_gds.get("gds_filename", "testfile.gds")
        output_path = output_dir / gds_filename

        print(f"Writing generated design layout to: {output_path}")
        self.geometry.write_gds(str(output_path))