import logging
import numpy as np
import gdstk as gp
import pysonnet

sonnet_file_path = "/home/ignacio/Sonnet/EM_sims/feedline.son"
path_to_sonnet = "/localdata/sonnet/18.56/"

# Set up logging to the console
log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

#Geometric constants
box_x,box_y = 100, 100 # size of the box
width = 5 # transmission line width
layer = 0 # layer for gds format
datatype = 1 # datatype for gds format

# Initialize the path
path = gp.RobustPath(initial_point=(box_x/3, 0), width=width, layer=layer, datatype=datatype)

# Define the cosine path and it's derivative
def path_function(t):
    return -box_x / 6 * (np.cos(np.pi * t) - 1), t * box_y

def d_path_function(t):
    return np.pi * box_x / 6 * np.sin(np.pi * t), box_y

path.parametric(path_function, path_gradient=d_path_function)

# Add the path to a cell
lib = gp.Library()
cell = lib.new_cell('feedline')
cell.add(path)

# Show the result
lib.write_gds("feedline.gds")
# The GeometryProject is the most basic Sonnet project type
project = ps.GeometryProject()

project['control']['res_detection'] = False

# The default length unit for Sonnet is mils,so let's change it
project.set_units(length='um')

# Then we can set up the box
project.setup_box(box_x, box_y, 200, 200)

# Define the metal types and if they are on the box top/bottom
# high kinetic inductance superconductor
project.define_metal("general", "PtSi", ls =21)
# low kinetic inductance superconductor
project.define_metal("general", "Nb", ls=0.08)
project.set_box_cover("free space", top=True)
project.set_box_cover("free space", bottom=True)

# Let's add a dielectric layer under the microstrip and air above
project.add_dielectric("air", layer, thickness=1000)
project.add_dielectric("silicon", layer + 1, thickness=100,
                       epsilon=11.9, dielectric_loss=0.004,
                       conductivity=4.4e-4)

# We can also define technology layers
project.define_technology_layer("metal", "microstrip", layer,
                                "PtSi", fill_type="diagonal")

# We also might want to see the current density
# project.set_options(current_density=True)

# Load the geometry into a pysonnet project
polygons = cell.get_polygons()
microstrip_polygons = [
    p.points for p in polygons
    if p.layer == layer and p.datatype == datatype
]

# Adding polygons and ports
project.add_polygons("metal", microstrip_polygons,
                     tech_layer="microstrip")
project.add_port("standard", 1, 2 * box_x / 3, box_y,
                 resistance=50)
project.add_port("standard", 2, 2 * box_x / 3, 0,
                 resistance=50)

# Add the frequency sweep to the project
project.add_frequency_sweep("abs", f1=4, f2=5)
# Select an analysis
project.set_analysis("frequency sweep")
# Make the sonnet file
project.make_sonnet_file(sonnet_file_path)
# Locate Sonnet
project.locate_sonnet(path_to_sonnet)
# Run the project
project.run("frequency sweep")

