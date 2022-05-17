from scipy.spatial.transform import Rotation


class Segment:
    def __init__(self, length: float, position: tuple[float, float, float], rotation: Rotation) -> None:
        self.length = length
        self.position = position
        self.rotation = rotation

    def __repr__(self):
        return f"Segment({self.position}, {self.rotation.as_rotvec()})"
