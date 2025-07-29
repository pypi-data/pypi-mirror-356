from GameTheoryLab.axelrod_interactive.strategy import Strategy

class Gradual(Strategy):
    """Class that implements the Gradual strategy. See the provided documentation for details."""
    def __init__(self):
        super().__init__()
        self.punishment = 0
        self.anger = 0

        self.name = "Gradual"
        self.__doc__ = ("This strategy works by punishing every defection with an increasing sequence of defections, "
                        "then returning to cooperation.")

    def additional_prep(self):
        self.punishment = 0
        self.anger = 0

    def update_history(self, opp_history, self_history):
        if not opp_history[-1] and self.punishment == 0:
            self.anger += 1
            self.punishment = self.anger

    def move(self, opp_history, self_history, opp_score, self_score):
        if self.punishment > 0:
            self.punishment -= 1
            return False
        return True


