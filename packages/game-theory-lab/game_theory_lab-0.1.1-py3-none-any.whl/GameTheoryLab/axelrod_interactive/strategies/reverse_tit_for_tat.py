from GameTheoryLab.axelrod_interactive.strategy import Strategy

class ReverseTitForTat(Strategy):
    """Class that implements the Reverse Tit for Tat strategy."""
    def __init__(self):
        super().__init__()
        self.name = "Reverse Tit for Tat"
        self.__doc__ = ("Similar with Tit for Tat. However, this strategies starts off by defecting, and then plays "
                        "the reverse of the opponents' last move (so if the opponent defects, it cooperates, "
                        "and if the opponent cooperates, it defects).")

    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history:
            return False
        return not opp_history[-1]