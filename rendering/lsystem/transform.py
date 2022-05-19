import pygmsh
import numpy as np
import numpy.typing as npt


class Transform:
    """Base class for objects that have a position and a rotation"""

    def __init__(self, position: npt.NDArray = np.array([0.0, 0.0, 0.0]), rotation: npt.NDArray = np.array([0.0, 0.0, 0.0])) -> None:
        self.position = position
        self.rotation = rotation

    def rotation_matrix(self) -> npt.NDArray:
        return pygmsh.rotation_matrix((1, 0, 0), self.rotation[0]) @ \
            pygmsh.rotation_matrix((0, 1, 0), self.rotation[1]) @ \
            pygmsh.rotation_matrix((0, 0, 1), self.rotation[2])

    def __repr__(self):
        return f"Transform({self.position}, {self.rotation})"
