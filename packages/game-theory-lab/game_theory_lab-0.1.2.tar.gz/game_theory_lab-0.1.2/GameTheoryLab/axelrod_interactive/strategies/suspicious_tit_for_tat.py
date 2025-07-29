from GameTheoryLab.axelrod_interactive.strategy import Strategy

class SuspiciousTitForTat(Strategy):
    """Class that implements the Suspicious Tit for Tat strategy. See the provided documentation for details."""
    def __init__(self):
        super().__init__()
        self.name = "Suspicious Tit for Tat"
        self.__doc__ = ("Similar with Tit for Tat. However, this strategies starts off by defecting, and then just "
                        "plays the opponents last move.")

    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history:
            return False
        return opp_history[-1]