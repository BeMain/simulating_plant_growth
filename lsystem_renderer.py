from lsystem import Controls, LSystem


class LSystemRenderer:
    """Uses a LSystem to generate instructions, and then renders a mesh based on those instructions."""

    def __init__(self, type: str = "LSystem", branching_angle: float = None, phyllotactic_angle: float = None, controls: dict[str, str] = None, axiom: str = None, rules: dict[str, str] = None) -> None:
        self.branching_angle = branching_angle
        self.phyllotactic_angle = phyllotactic_angle
        self.controls = Controls(**controls)
        self.lsystem = LSystem(axiom, rules)
