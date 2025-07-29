from GameTheoryLab.axelrod_interactive.strategy import Strategy

class TitForTat(Strategy):
    """Class that implements the Tit for Tat strategy."""
    def __init__(self):
        super().__init__()
        self.name = "Tit for Tat"
        self.__doc__ = "This strategies starts off by cooperating, and then just plays the opponents last move."

    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history:
            return True
        return opp_history[-1]