from copy import deepcopy
from math import radians
import pygmsh
import numpy.typing as npt

from rendering.lsystem.transform import Transform


from .lsystem import LSystem
from .segment import Segment


class LSystemRenderer:
    """Uses a LSystem to generate instructions, and then renders a mesh based on those instructions."""

    def __init__(self, type: str = "LSystem", branching_angle: float = None, phyllotactic_angle: float = None, controls: dict[str, str] = None, axiom: str = None, rules: dict[str, str] = None) -> None:
        self.branching_angle = branching_angle
        self.phyllotactic_angle = phyllotactic_angle
        self.controls = {value: key for key, value in controls.items()}
        self.rotation_matrices = self.get_rotation_matrices(controls)
        self.lsystem = LSystem(axiom, rules)

        self.state = Transform()

    def get_rotation_matrices(self, controls) -> dict[str, npt.NDArray]:
        angle = radians(10)
        return {
            controls["right"]: (0, 0, -angle),
            controls["left"]: (0, 0, angle),

            controls["up"]: (0, -angle, 0),
            controls["down"]: (0, angle, 0),

            controls["roll_right"]: (-angle, 0, 0),
            controls["roll_left"]: (angle, 0, 0)
        }

    def generate_segments(self) -> list[Segment]:
        """Generates a list of Segments based on lsystem.axiom, using self.controls."""
        segments = []

        segment_length: int = 0
        states: list[Transform] = []

        for instruction in self.lsystem.axiom:
            if not instruction in self.controls:  # Increase length of next segment
                segment_length += 1

            else:
                if segment_length >= 1:  # Create new segment
                    segments.append(
                        deepcopy(Segment(segment_length, self.state.position, self.state.rotation)))
                    self.state.position += self.state.rotation_matrix() @ \
                        [segment_length, 0, 0]

                    segment_length = 0

                if self.controls[instruction] == "save_state":  # Save state
                    states.append(deepcopy(self.state))
                elif self.controls[instruction] == "pop_state":  # Pop state
                    self.state = states.pop()

                else:  # Apply rotation
                    self.state.rotation += self.rotation_matrices[instruction]

        return segments

    def generate_mesh(self):
        """Generate a mesh based on Segments from generate_segments()"""
        segments = self.generate_segments()
        with pygmsh.occ.Geometry() as geom:
            #geom.characteristic_length_max = 0.1
            for segment in segments:
                cyl = geom.add_cylinder(
                    segment.position, segment.rotation_matrix() @ [segment.length, 0, 0], 0.3)

            mesh = geom.generate_mesh()
            mesh.write("test.vtk")
            pygmsh.helpers.gmsh.fltk.run()
