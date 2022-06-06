import numpy as np
import numpy.typing as npt


class Transform:
    """Base class for objects that have a position and a rotation"""

    def __init__(self, position: npt.NDArray = np.array([0.0, 0.0, 0.0]), rotation: npt.NDArray = np.array([0.0, 0.0, 0.0])) -> None:
        self.position = position
        self.rotation = rotation

    @property
    def rotation_matrix(self) -> npt.NDArray:
        return rotation_matrix((1, 0, 0), self.rotation[0]) @ \
            rotation_matrix((0, 1, 0), self.rotation[1]) @ \
            rotation_matrix((0, 0, 1), self.rotation[2])

    @property
    def normal_vector(self) -> npt.NDArray:
        return self.rotation_matrix @ [1, 0, 0]

    def __repr__(self):
        return f"Transform({self.position}, {self.rotation})"


def rotation_matrix(u, theta):
    """Return matrix that implements the rotation around the vector :math:`u`
    by the angle :math:`\\theta`, cf.
    https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle.

    :param u: rotation vector
    :param theta: rotation angle
    """
    assert np.isclose(np.inner(u, u), 1.0), "the rotation axis must be unitary"

    # Cross-product matrix.
    cpm = np.array(
        [[0.0, -u[2], u[1]], [u[2], 0.0, -u[0]], [-u[1], u[0], 0.0]])
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.eye(3) * c + s * cpm + (1.0 - c) * np.outer(u, u)
    return R
