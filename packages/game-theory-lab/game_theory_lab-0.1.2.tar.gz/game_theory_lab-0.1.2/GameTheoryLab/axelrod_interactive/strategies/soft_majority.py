from GameTheoryLab.axelrod_interactive.strategy import Strategy

class SoftMajority(Strategy):
    """Class that implements the Soft Majority strategy."""
    def __init__(self):
        super().__init__()
        self.name = "Soft Majority"
        self.__doc__ = ("This strategy starts by cooperating, and cooperates if the opponent cooperates at least as "
                        "much as it defects, and defects otherwise.")

    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history:
            return True
        return self.opps_coop_count >= self.opps_defect_count
