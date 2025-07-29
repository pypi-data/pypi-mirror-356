from GameTheoryLab.axelrod_interactive.strategy import Strategy

class Tranquilizer(Strategy):
    """Class that implements the Tranquilizer strategy. See the provided documentation for details.

    Args:
        period (int): The length of the strategy's initial cooperation period. Defaults to 5.
    """
    def __init__(self, period=5):
        # Validation
        if not isinstance(period, int):
            raise ValueError(f"Can you cooperate a fractional number of times? (You entered period = {period}).")

        super().__init__()
        self.period = period
        self.counter = 0

        self.name = f"Tranquilizer (period = {self.period})"
        self.__doc__ = ("One of the sneakiest strategies yet, the tranquilizer starts off by cooperating, then defects "
                        "periodically to exploit kindness. If it perceives more-than-normal defection, "
                        "the cooperation period is reduced until it reaches 2.")

    def update_history(self, opp_history, self_history):
        if not opp_history: return

        if not opp_history[-1]:
            self.opps_defect_count += 1
        if self.counter == 0:
            if self.opps_defect_count > 1 + int(not opp_history[-1]):
                if self.period > 1:
                    self.period -= 1
            self.opps_defect_count = 0

    def move(self, opp_history, self_history, opp_score, self_score):
        if self.counter < self.period:
            self.counter += 1
            return True

        self.counter = 0
        return False
