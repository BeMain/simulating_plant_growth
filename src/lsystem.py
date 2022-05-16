
class Controls():
    def __init__(self, right: str = "+", left: str = "-", up: str = "^", down: str = "&", rollRight: str = ">", rollLeft: str = "<"):
        self.right = right
        self.left = left
        self.up = up
        self.down = down
        self.rollRight = rollRight
        self.rollLeft = rollLeft


class LSystem:
    def __init__(self, axiom: str, rules: dict[str, str], controls: Controls = Controls()):
        """Create a L System based on an [axiom] and a set of [rules].

        Optionally, [controls] can be specified. These map instructions from the L System to the final rendered output.
        """

        self.controls = controls
        self.axiom = axiom
        self.rules = rules

    def step(self):
        """Apply the rules to the axiom, and replace axiom with the result."""

        self.axiom = "".join([(self.rules[i] if i in self.rules else i)
                              for i in self.axiom])
