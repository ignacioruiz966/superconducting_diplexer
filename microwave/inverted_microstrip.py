import gdsfactory as gf

class InvertedMicrostrip:

    def __init__(self, name, width, length, layer):
        self.name = name
        self.width = width
        self.length = length
        self.layer = layer


    def describe(self):

        return ("Inverted Microstrip\n"
                f"Design Name: {self.name}\n"
                f"Width: {self.width} um\n"
                f"Length: {self.length} um\n"
                f"Layer: {self.layer[0]}")


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





"""
@gf.cell
def inverted_microstrip(length: float, width: float):

    c = gf.Component()

    x0,x1 = 0.0, length
    y0,y1 = -width/2.0, width/2.0
    trace = gf.components.rectangle(
        size=(length,width),
        layer=LAYER["TiN"],
    )
    trace_ref = c << trace
    trace.movey(0,0)

    c.add_port(
        name="o1",
        center=(x0,0),
        width=width,
        orientation=180,
        layer=LAYER["Ports"],
        port_type="optical"
    )
    c.add_port(
        name="o2",
        center=(x1,0),
        width=width,
        orientation=-0,
        layer=LAYER["Ports"],
        port_type="optical"
    )

    return c

"""