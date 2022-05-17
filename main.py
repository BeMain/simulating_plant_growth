from rendering.lsystem.lsystem_renderer import LSystemRenderer
import yaml


with open("fagus_sylvatica.yaml", "r") as file:
    data = yaml.safe_load(file)

renderer = LSystemRenderer(**data["rendering"]["stem"])

for _ in range(1):
    renderer.lsystem.step()
print(renderer.lsystem.axiom)

segments = renderer.generate_segments()

print(segments)
