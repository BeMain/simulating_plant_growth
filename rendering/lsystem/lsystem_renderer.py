from copy import deepcopy
from math import radians
import pyvista as pv
import numpy as np
import numpy.typing as npt

from rendering.lsystem.transform import Transform


from .lsystem import LSystem
from .segment import Segment


class RenderState(Transform):
    def __init__(self, position: npt.NDArray = np.array([0.0, 0.0, 0.0]), rotation: npt.NDArray = np.array([0.0, 0.0, 0.0]), diameter: float = 0.5) -> None:
        super().__init__(position, rotation)

        self.diameter = diameter


class LSystemRenderer:
    """Uses a LSystem to generate instructions, and then renders a mesh based on those instructions."""

    def __init__(self, type: str = "LSystem",
                 branching_angle: float = None,
                 base_diameter: float = None,
                 diameter_ratio: float = None,
                 controls: dict[str, str] = None,
                 axiom: str = None,
                 rules: dict[str, str] = None,
                 ) -> None:
        """
        @param diameter_ratio: How the diameter should change from start to end of Segment, as fraction.
        @param controls: How instructions from the LSystem should be mapped to different actions when creating Segments.
        @param axoim: Axiom for LSystem to use.
        @param rules: Rules for LSystem to use.
        """

        self.branching_angle = branching_angle
        self.diameter_ratio = diameter_ratio
        self.controls = {value: key for key, value in controls.items()}
        self.rotation_vectors = self.get_rotation_vectors(controls)
        self.lsystem = LSystem(axiom, rules)

        self.state = RenderState(diameter=base_diameter)

    def get_rotation_vectors(self, controls) -> dict[str, npt.NDArray]:
        angle = radians(self.branching_angle)
        return {
            controls["right"]: (0, 0, -angle),
            controls["left"]: (0, 0, angle),

            controls["up"]: (0, -angle, 0),
            controls["down"]: (0, angle, 0),

            controls["roll_right"]: (-angle, 0, 0),
            controls["roll_left"]: (angle, 0, 0)
        }

    def generate_segments(self) -> list[Segment]:
        """Generate a list of Segments based on lsystem.axiom, using self.controls."""
        segments = []

        segment_length: int = 0
        states: list[RenderState] = []

        for instruction in self.lsystem.axiom:
            if not instruction in self.controls:  # Increase length of next segment
                segment_length += 1

            else:
                if segment_length >= 1:  # Create new segment
                    diameter_mod = pow(self.diameter_ratio, segment_length)
                    segments.append(deepcopy(
                        Segment(segment_length,
                                self.state.diameter,
                                self.state.diameter * diameter_mod,
                                self.state.position,
                                self.state.rotation,
                                )
                    ))
                    self.state.position += self.state.normal_vector * segment_length
                    self.state.diameter *= diameter_mod

                    segment_length = 0

                if self.controls[instruction] == "save_state":  # Save state
                    states.append(deepcopy(self.state))
                elif self.controls[instruction] == "pop_state":  # Pop state
                    self.state = states.pop()

                else:  # Apply rotation
                    self.state.rotation += self.rotation_vectors[instruction]

        return segments

    def generate_mesh(self, resolution=10):
        """Generate a mesh based on Segments from generate_segments()"""
        segments = self.generate_segments()

        p = pv.Plotter()
        for segment in segments:
            # Calculate length to get correct bottom_d
            cone_l = segment.top_d * segment.length / \
                (segment.top_d - segment.bottom_d)
            # Create cone mesh
            cone = pv.Cone(
                segment.position +
                segment.normal_vector * cone_l / 2,
                segment.normal_vector,
                cone_l,
                segment.top_d,
                capping=False,
                resolution=resolution)

            # Clip cone to correct length
            res = cone.clip(
                segment.normal_vector,
                segment.position +
                segment.normal_vector * segment.length,
            )

            p.add_mesh(res)

        p.show()
