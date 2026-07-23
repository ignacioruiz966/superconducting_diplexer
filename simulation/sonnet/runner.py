import subprocess
from pathlib import Path


class SonnetRunner:
    def __init__(self, output_config, em_path: str = "em"):
        self.em_path = em_path
        self.project_path = Path(output_config["sonnet_directory"]).resolve()
        self.son_path = output_config["son_filename"]

    def run_simulation(self, timeout: float = 1800) -> Path:
        if not self.project_path.exists():
            raise FileNotFoundError(f"Project directory not found: {self.project_path}")

        son_project_path = self.project_path / self.son_path
        if not son_project_path.exists():
            raise FileNotFoundError(f"Sonnet project file not found: {son_project_path}")

        s2p_file = son_project_path.with_suffix(".s2p")

        cmd = [self.em_path, "-S", str(son_project_path)]
        print(f"Starting Sonnet simulation for {self.son_path}...")

        try:
            subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.CalledProcessError as e:
            error_log = e.stderr if e.stderr else e.stdout
            raise RuntimeError(f"Sonnet simulation failed: \n{error_log}") from e
        except subprocess.TimeoutExpired as e:
            raise TimeoutError(f"Simulation timed out after {timeout}s") from e

        print(f"Extracting S-parameter data to {s2p_file.name}...")

        if not s2p_file.exists():
            raise FileNotFoundError(f"S2P file was not created: {s2p_file}")

        return s2p_file
