import argparse
from pathlib import Path
import yaml
import gdsfactory as gf
from read_config import config_file



"""
from microwave.inverted_microstrip import inverted_microstrip

def main(config_path):

    c = gf.Component()

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    length = float(cfg["trace"]["length"])
    width = float(cfg["trace"]["width"])

    c = inverted_microstrip(length=length, width=width)

    out_dir = Path("gds")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{cfg['design']['name']}.gds"
    c.write_gds(out_file)

    print(f"GDS written to: {out_file.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to YAML config")
    args = parser.parse_args()
    main(args.config)


"""