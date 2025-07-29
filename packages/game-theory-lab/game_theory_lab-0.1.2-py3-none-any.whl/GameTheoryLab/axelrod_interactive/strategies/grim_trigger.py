from GameTheoryLab.axelrod_interactive.strategy import Strategy

class GrimTrigger(Strategy):
    """Class that implements the Grim Trigger strategy."""
    def __init__(self):
        super().__init__()
        self.name = "Grim Trigger"
        self.__doc__ = ("This strategy cooperates continually, until the opponent defects once, and then defects for "
                        "the remainder of the game.")

    def move(self, opp_history, self_history, opp_score, self_score):
        return self.opps_defect_count == 0
