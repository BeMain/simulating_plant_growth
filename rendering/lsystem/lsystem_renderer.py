from copy import deepcopy
from math import radians, cos, sin
import pygmsh
import numpy as np

from .lsystem import LSystem
from .segment import Segment

from scipy.spatial.transform import Rotation


class RendererState:
    def __init__(self, position: np.ndarray = [0.0, 0.0, 0.0], rotation: Rotation = Rotation.from_rotvec([0, 0, 0])) -> None:
        self.position = position
        self.rotation = rotation


class LSystemRenderer:
    """Uses a LSystem to generate instructions, and then renders a mesh based on those instructions."""

    def __init__(self, type: str = "LSystem", branching_angle: float = None, phyllotactic_angle: float = None, controls: dict[str, str] = None, axiom: str = None, rules: dict[str, str] = None) -> None:
        self.branching_angle = branching_angle
        self.phyllotactic_angle = phyllotactic_angle
        self.controls = {value: key for key, value in controls.items()}
        self.rotation_matrices = self.get_rotation_matrices(controls)
        self.lsystem = LSystem(axiom, rules)

        self.state = RendererState()

    def get_rotation_matrices(self, controls):
        angle = radians(10)
        return {
            controls["right"]: self._ru(-angle),
            controls["left"]: self._ru(angle),

            controls["up"]: self._rl(-angle),
            controls["down"]: self._rl(angle),

            controls["roll_right"]: self._rh(-angle),
            controls["roll_left"]: self._rh(angle),
        }

    def _ru(self, a):
        return Rotation.from_matrix([[cos(a),   sin(a), 0],
                                     [-sin(a),  cos(a), 0],
                                     [0,        0,      1]])

    def _rl(self, a):
        return Rotation.from_matrix([[cos(a),   0,      -sin(a)],
                                     [0,        1,      0],
                                     [sin(a),   0,      cos(a)]])

    def _rh(self, a):
        return Rotation.from_matrix([[1,        0,      0],
                                     [0,        cos(a), -sin(a)],
                                     [0,        sin(a), cos(a)]])

    def generate_segments(self) -> list[Segment]:
        """Generates a list of Segments based on lsystem.axiom, using self.controls."""
        segments = []

        segment_length: int = 0
        states: list[RendererState] = []

        for instruction in self.lsystem.axiom:
            if not instruction in self.controls:  # Increase length of next segment
                segment_length += 1

            else:
                if segment_length >= 1:  # Create new segment
                    segments.append(
                        Segment(segment_length, deepcopy(self.state.position), self.state.rotation))
                    self.state.position += self.state.rotation.apply([
                        segment_length, 0, 0])

                    segment_length = 0

                if self.controls[instruction] == "save_state":  # Save state
                    states.append(deepcopy(self.state))
                elif self.controls[instruction] == "pop_state":  # Pop state
                    self.state = states.pop()

                else:  # Apply rotation
                    self.state.rotation = self.rotation_matrices[instruction] * \
                        self.state.rotation

        return segments

    def generate_mesh(self):
        """Generate a mesh based on Segments from generate_segments()"""
        segments = self.generate_segments()
        with pygmsh.occ.Geometry() as geom:
            #geom.characteristic_length_max = 0.1
            for segment in segments:
                cylinder = geom.add_cylinder(
                    [0.0, 0.0, 0.0], [segment.length, 0.0, 0.0], 0.3)

                # Apply rotation in three axis
                angles = segment.rotation.as_rotvec()
                geom.rotate(cylinder, (0, 0, 0), angles[0], (1, 0, 0))
                geom.rotate(cylinder, (0, 0, 0), angles[1], (0, 1, 0))
                geom.rotate(cylinder, (0, 0, 0), angles[2], (0, 0, 1))
                # Apply translation
                geom.translate(cylinder, segment.position)

            geom.generate_mesh()
            pygmsh.helpers.gmsh.fltk.run()
