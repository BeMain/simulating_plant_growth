import pygmsh
from rendering.lsystem.lsystem_renderer import LSystemRenderer
import yaml


with open("fagus_sylvatica.yaml", "r") as file:
    data = yaml.safe_load(file)

renderer = LSystemRenderer(**data["rendering"]["stem"])

for _ in range(3):
    renderer.lsystem.step()

renderer.generate_mesh()
