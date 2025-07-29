from GameTheoryLab.axelrod_interactive.strategy import Strategy

class AlwaysCooperate(Strategy):
    """Class that implements the Always Cooperate strategy."""
    def __init__(self):
        super().__init__()
        self.name = "Always Cooperate"
        self.__doc__ = "This is a simple strategy which starts by cooperating... and cooperates for the entire round."

    def move(self, opp_history, self_history, opp_score, self_score):
        return True