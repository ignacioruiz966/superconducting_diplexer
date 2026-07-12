from microwave.inverted_microstrip import InvertedMicrostrip
import gdsfactory as gf


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

print(line1.describe())
print(line2.describe())


line1.validate()
line2.validate()

two_strips = gf.Component()

component1 = line1.build()
component2 = line2.build()

ref1 = two_strips << component1
ref2 = two_strips << component2

ref1.movey(0,-10)
ref2.movey(0,10)

two_strips.write_gds("../gds/two_microstrips.gds")
