
"""
Pipeline orchestrator for the superconducting CAD framework.

This script acts as the single entry point to load configuration files,
instantiate technology processes, generate transmission line geometries,
and export the final layouts to GDSII files.
"""

from pathlib import Path
import sys

# Framework imports
from configs.design_config import DesignConfig
from microwave.inverted_microstrip import InvertedMicrostrip
from technology.process import Process
from utils.config_loader import load_config


def main() -> None:

    if len(sys.argv) != 2:
        raise SystemExit("Usage: python run_design.py <config_file>")

    config_path = Path(sys.argv[1])
    if not config_path.is_file():
        raise SystemExit(f"Error: Configuration file not found at '{config_path}'")

    print(f"Loading configuration from '{config_path}'")
    raw_config = load_config(config_path)

    config = DesignConfig(raw_config)

    print("Initializing fabrication process parameters...")
    process = Process.from_config(config.process)

    print("Building Inverted Microstrip geometry model...")
    microstrip = InvertedMicrostrip.from_config(config.geometry, process)

    print(microstrip.describe())
    microstrip.validate()

    component = microstrip.build()

    output_settings = config.output
    output_dir = Path(output_settings.get("directory","gds"))

    gds_filename = output_settings.get("gds_filename", "testfile.gds")

    output_path = output_dir / gds_filename

    print(f"Writing generated design layout to: {output_path}")
    component.write_gds(str(output_path))
    print("Pipeline execution completed successfully.")


if __name__ == "__main__":
    main()