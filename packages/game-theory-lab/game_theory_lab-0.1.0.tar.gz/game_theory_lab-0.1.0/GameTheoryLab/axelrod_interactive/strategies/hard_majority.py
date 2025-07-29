from GameTheoryLab.axelrod_interactive.strategy import Strategy

class HardMajority(Strategy):
    """Class that implements the Hard Majority strategy."""
    def __init__(self):
        super().__init__()
        self.name = "Hard Majority"
        self.__doc__ = ("This strategy starts by cooperating, and defects if the opponent defects at least as much as "
                        "it cooperates, and cooperates otherwise.")

    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history:
            return True
        return self.opps_coop_count > self.opps_defect_count