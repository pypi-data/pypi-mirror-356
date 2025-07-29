import random
from GameTheoryLab.axelrod_interactive.strategy import Strategy

class Joss(Strategy):
    """Class that implements the Joss strategy. See provided documentation for details.
    Args:
        prob_of_defection (float): Probability of defecting when the opponent cooperates. Defaults to 0.1. Note that it must be in (0, 1).
    """
    def __init__(self, prob_of_defection=0.1):
        # Validation
        if not 0 < prob_of_defection < 1:
            if prob_of_defection <= 0:
                string = f"({prob_of_defection} <= 0)"
            else:
                string = f"({prob_of_defection} >= 1)"
            raise ValueError(f"Parameter 'prob_of_defection' is not in range! " + string)

        super().__init__()
        self.prob_of_defection = prob_of_defection

        self.name = f"Joss (p = {self.prob_of_defection})"
        self.__doc__ = ("This strategy plays like Tit for Tat, except when the opponent cooperates, it sometimes "
                        "defects (precisely, with probability 'prob_of_defection').")

    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history:
            return True

        if not opp_history[-1]:
            return False

        return random.random() >= self.prob_of_defection
