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


with open("fagus_sylvatica.yaml", "r") as file:
    data = yaml.safe_load(file)

renderer = LSystemRenderer(**data["rendering"]["stem"])

for _ in range(1):
    renderer.lsystem.step()
print(renderer.lsystem.axiom)

segments = renderer.generate_segments()

print(segments)
