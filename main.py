import pygmsh
from lsystem_renderer import LSystemRenderer
from lsystem import *
import yaml


lsys = LSystem("F", {
    "F": "Y[++++++MF][-----NF][^^^^^OF][&&&&&PF]",
    "M": "Z-M",
    "N": "Z+N",
    "O": "Z&O",
    "P:": "Z^P",
    "Y": "Z-ZY+",
    "Z": "ZZ",
},)


for _ in range(3):
    lsys.step()


with open("fagus_sylvatica.yaml", "r") as file:
    data = yaml.safe_load(file)

renderer = LSystemRenderer(**data["rendering"]["stem"])
print(renderer)


with pygmsh.occ.Geometry() as geom:
    geom.characteristic_length_max = 0.1
    ellipsoid = geom.add_ellipsoid([0.0, 0.0, 0.0], [1.0, 0.7, 0.5])

    cylinders = [
        geom.add_cylinder([-1.0, 0.0, 0.0], [2.0, 0.0, 0.0], 0.3),
        geom.add_cylinder([0.0, -1.0, 0.0], [0.0, 2.0, 0.0], 0.3),
    ]
    geom.boolean_difference(ellipsoid, geom.boolean_union(cylinders))

    mesh = geom.generate_mesh()

    pygmsh.helpers.gmsh.fltk.run()
