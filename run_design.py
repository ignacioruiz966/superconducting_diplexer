
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
from geometry.export.gds_export import GdsExport
from geometry.geometry_factory import GeometryFactory
from simulation.simulation_config import SimulationConfig
from simulation.sonnet.project import SonnetProject
from simulation.sonnet.runner import SonnetRunner
from simulation.sonnet.results import SonnetResults
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

    print("Building Inverted SIR geometry model...")
    sir = GeometryFactory.create(config.geometry, process)
    component = sir.build()

    gds = GdsExport(config.output, component)
    gds.export()

    print("Pipeline execution completed successfully.")

    print("Initializing simulation process parameters...")
    sim_config = SimulationConfig.from_config(config.simulation)

    project = SonnetProject(process, sim_config, sir)

    print("Initializing Sonnet Project")
    project.setup_simulation()

    runner = SonnetRunner(sim_config.output, em_path="em")

    s2p_output_path = runner.run_simulation( timeout=1800.0)

    print(f"Simulation complete. Output saved to: {s2p_output_path.name}")

    results = SonnetResults(s2p_path=s2p_output_path)

    f_res = results.extract_resonant_frequency()
    q_factor = results.calculate_q_factor()

    print(f"\n--- Analysis Results ---")
    print(f"Resonant Frequency: {f_res / 1e9:.4f} GHz")
    print(f"Loaded Q-Factor:    {q_factor:.2f}")

    # 5. Visualize the data
    results.plot_s_parameters(save_path=sim_config.output["sonnet_directory"])
    print("Plot saved to disk.")







if __name__ == "__main__":
    main()