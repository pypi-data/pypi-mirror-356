from GameTheoryLab.axelrod_interactive.strategy import Strategy

class TitForKTats(Strategy):
    """Class that implements the Tit for 'K' Tats strategy. See the provided documentation for details.
    Args:
        k (int): Number of defects by opponent that warrants a defect from the strategy (number of tats for one tit). Defaults to 2.
    """
    def __init__(self, k: int=2):
        # Validation
        if not isinstance(k, int):
            raise ValueError(f"Can you defect a fractional number of times? (You entered k = {k}.)")
        super().__init__()
        self.k = k
        self.counter = self.k
        self.name = f"Tit for {self.k} tats"
        self.__doc__ = (f"This strategy is similar to Tit for Tat, with the slight variation that a defect (tit) is "
                        f"played after {self.k} defects in a row ({self.k} tats).")

    def additional_prep(self):
        self.counter = self.k

    def update_history(self, opp_history, self_history):
        if opp_history:
            if not opp_history[-1] and self.counter > 0:
                self.counter -= 1
            else:
                self.counter = self.k

    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history or self.counter > 0:
            return True

        self.counter = self.k
        return False