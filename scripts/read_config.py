import yaml
from pathlib import Path

config_file = Path("../configs/cpw.yaml")
with open(config_file, "r") as file:
    config = yaml.safe_load(file)
