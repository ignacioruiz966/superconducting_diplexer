from geometry.inverted_microstrip import InvertedMicrostrip
import gdsfactory as gf



two_strips = gf.Component()
spacing = 20

line1 = InvertedMicrostrip(
    name="validation",
    width=2.7,
    length=100,
    layer=(1,0),
)

line2 = InvertedMicrostrip(
    name="validation",
    width=2.7,
    length=100,
    layer=(1,0),
)

line1.describe()
line2.describe()

line1.validate()
line2.validate()


component1 = line1.build()
component2 = line2.build()

ref1 = two_strips << component1
ref2 = two_strips << component2

ref2.movey(spacing + line2.width)

two_strips.write_gds("../gds/two_microstrips.gds")
