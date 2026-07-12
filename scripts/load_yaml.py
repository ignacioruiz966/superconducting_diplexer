import yaml

with open ("../configs/ims_line.yaml", "r") as file:
    ims_line = yaml.safe_load(file)

print(ims_line)