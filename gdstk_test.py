import gdsfactory as gf
from qpdk import PDK

PDK.activate()

# Create a transmon qubit
from qpdk.cells.transmon import transmon

qubit = transmon(pad_gap=15)
qubit.plot()

from gdsfactory.read import from_yaml
from qpdk import tech

chip = from_yaml(
    "qpdk/samples/qubit_test_chip.pic.yml",
    routing_strategies=tech.routing_strategies,
)

chip.show()