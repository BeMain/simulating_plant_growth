import numpy as np
import numpy.typing as npt


class Segment:
    def __init__(self, length: float, position: npt.NDArray = np.array([0.0, 0.0, 0.0]), rotation: npt.NDArray = np.array([0.0, 0.0, 0.0])) -> None:
        self.length = length
        self.position = position
        self.rotation = rotation

    def __repr__(self):
        return f"Segment({self.position}, {self.rotation})"
