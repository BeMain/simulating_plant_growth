
class Controls():
    def __init__(self, right: str = "+", left: str = "-", up: str = "^", down: str = "&", roll_right: str = ">", roll_left: str = "<"):
        self.right = right
        self.left = left
        self.up = up
        self.down = down
        self.roll_right = roll_right
        self.roll_left = roll_left


class LSystem:
    def __init__(self, axiom: str, rules: dict[str, str]):
        """Create a LSystem based on an [axiom] and a set of [rules]."""

        self.axiom = axiom
        self.rules = rules

    def step(self):
        """Apply the rules to the axiom, and replace axiom with the result."""

        self.axiom = "".join([(self.rules[i] if i in self.rules else i)
                              for i in self.axiom])
