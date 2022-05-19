import numpy as np
import numpy.typing as npt
import pygmsh

from rendering.lsystem.transform import Transform


class Segment(Transform):
    def __init__(self, length: float, top_diameter: float, bottom_diameter: float, position: npt.NDArray = np.array([0.0, 0.0, 0.0]), rotation: npt.NDArray = np.array([0.0, 0.0, 0.0])) -> None:
        super().__init__(position, rotation)

        self.length = length
        self.top_d = top_diameter
        self.bottom_d = bottom_diameter

    def __repr__(self):
        return f"Segment({self.length}; {self.position}, {self.rotation})"
