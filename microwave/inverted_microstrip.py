import gdsfactory as gf
from technology.process import Process


class InvertedMicrostrip:

    def __init__(self, name, width, length, layer, process):
        self.name = name
        self.width = width
        self.length = length
        self.layer = layer
        self.process = process


    def describe(self):
        divider = "=" * 40

        geo = (
                f"\n{divider}\n"
                "Inverted Microstrip\n"
                f"{divider}\n"
                f"Design Name: {self.name}\n"
                f"Width: {self.width} um\n"
                f"Length: {self.length} um\n"
                f"Layer: {self.layer[0]}\n")

        pro = (
                f"\n{divider}\n"
                f"Process\n"
                f"{divider}\n"
                f"Substrate: {self.process.substrate}\n"
                f"Conductor: {self.process.conductor}\n"
                f"Dielectric: {self.process.dielectric}\n"
                f"Ground Plane: {self.process.ground}\n")

        return geo + pro


    def build(self):

        component = gf.Component()

        rectangle = gf.components.rectangle(
            size=(self.length,self.width),
            layer=self.layer,
        )

        component << rectangle

        return component

    def validate(self):
        if self.width <= 0 or self.length <= 0:
            raise ValueError("The dimensions of the rectangle cannot be negative")

        if not isinstance(self.layer, tuple):
            raise TypeError("The layer must be tuple")

        if self.name is None or self.name == "":
            raise ValueError("The name cannot be empty")

    @classmethod
    def from_config(cls, config: dict, process: Process) -> "InvertedMicrostrip":

        geometry_type = config.get("type")

        if geometry_type != "inverted_microstrip":
            raise TypeError(f"Invalid geometry type: '{geometry_type}'. Expected 'inverted_microstrip'")


        if not isinstance(config, dict):
            raise TypeError("The configuration must be a dictionary")

        name = config.get("name")
        width = config.get("width")
        length = config.get("length")

        if name is None or width is None or length is None:
            raise ValueError(
                "Configuration missing required fields: 'name', 'width', 'length'"
            )

        try:
            width = float(width)
            length = float(length)

            if width <= 0 or length <= 0:
                raise ValueError("The dimensions of the rectangle cannot be negative")

        except ValueError:
            raise ValueError(
                f"Width and length must be valid numeric values. Got width={width}, length={length}"
            )

        return cls(
            name=name,
            width=width,
            length=length,
            layer=process.conductor_layer,
            process=process
        )
