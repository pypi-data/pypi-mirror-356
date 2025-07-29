from GameTheoryLab.axelrod_interactive.strategy import Strategy

class SoftGrim(Strategy):
    """Class that implements the Soft Grim strategy. See the provided documentation for details.

    Args:
        beef_period (int): The period during which the strategy defects as a result of the opponent's prior defection.
    """
    def __init__(self, beef_period: int=100):
        # Validation
        if not isinstance(beef_period, int):
            raise ValueError(f"Can you defect a fractional number of times? (You entered {beef_period}.)")
        super().__init__()
        self.beef_period = beef_period
        self.name = f"Soft Grim (period = {self.beef_period})"
        self.__doc__ = ("This strategy is like Grim Trigger, but it cooperates after a long period, as specified by "
                        "'beef_period'.")
        self.beef = 0

    def additional_prep(self):
        self.beef = 0

    def update_history(self, opp_history, self_history):
        if opp_history and not opp_history[-1]:
            if self.beef == 0 and self_history[-1]: self.beef = self.beef_period

    def move(self, opp_history, self_history, opp_score, self_score):
        if self.beef > 0:
            self.beef -= 1
            return False
        return True


