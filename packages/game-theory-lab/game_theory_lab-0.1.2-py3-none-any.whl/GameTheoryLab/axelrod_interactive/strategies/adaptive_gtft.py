import random
from GameTheoryLab.axelrod_interactive.strategy import Strategy

class AdaptiveGTFT(Strategy):
    """Class that implements the Adaptive GTFT (Generous Tit for Tat) strategy. See provided documentation for details.

    Args:
        base_generosity (float): Initial probability of forgiving a defection. Must be in (0, 1).
        delta_p (float): Parametrizes how sensitive the strategy's 'generosity' is to perceived cooperation/defection. Must also be in (0, 1).
    """
    def __init__(self, base_generosity: float=0.5, delta_p: float=0.1):
        # Validation
        if not 0 < base_generosity < 1:
            if base_generosity <= 0:
                string = f"({base_generosity} <= 0)"
            else:
                string = f"({base_generosity} >= 1)"
            raise ValueError("Parameter 'base_generosity' is out of range! " + string)
        if not 0 < delta_p < 1:
            if delta_p <= 0:
                string = f"({delta_p} <= 0)"
            else:
                string = f"({delta_p} >= 1)"
            raise ValueError("Parameter 'delta_p' is out of range! " + string)

        super().__init__()
        self.delta_p = delta_p
        self.base_generosity = base_generosity
        self.prob_of_cooperation = base_generosity

        self.name = f"Adaptive G-TFT (p = {self.prob_of_cooperation:.3f}, dp = {self.delta_p:.3f})"
        self.__doc__ = ("This strategy is just like Generous Tit for Tat, but the chances of it forgiving future "
                        "defections are increased with each cooperation (and decreased with each defection), "
                        "as parameterized by 'delta_p'. Note that both 'base_generosity' and 'delta_p' must be "
                        "between 0 and 1.")

    def additional_prep(self):
        self.prob_of_cooperation = self.base_generosity

    def update_history(self, opp_history, self_history):
        if opp_history:
            if opp_history[-1]:
                self.prob_of_cooperation += (1 - self.prob_of_cooperation) * self.delta_p
            else:
                self.prob_of_cooperation -= self.prob_of_cooperation * self.delta_p

    def move(self, opp_history, self_history, opp_score, self_score):
        if opp_history and not opp_history[-1]:
            return random.random() >= self.prob_of_cooperation
        return True

