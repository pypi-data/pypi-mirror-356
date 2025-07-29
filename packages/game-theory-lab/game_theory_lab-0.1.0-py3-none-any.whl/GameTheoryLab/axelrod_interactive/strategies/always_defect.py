from GameTheoryLab.axelrod_interactive.strategy import Strategy

class AlwaysDefect(Strategy):
    """Class that implements the Always Defect strategy."""
    def __init__(self):
        super().__init__()
        self.name = "Always Defect"
        self.__doc__ = "This is a simple strategy that starts by defecting, and defects for the entire round."

    def move(self, opp_history, self_history, opp_score, self_score):
        return False