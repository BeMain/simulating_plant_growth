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

renderer = LSystemRenderer.from_yaml(data["rendering"]["stem"])
print(renderer)
