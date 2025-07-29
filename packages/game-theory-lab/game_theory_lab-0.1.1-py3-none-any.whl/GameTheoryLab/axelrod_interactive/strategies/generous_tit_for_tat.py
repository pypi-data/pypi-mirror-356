import random
from GameTheoryLab.axelrod_interactive.strategy import Strategy

class GenerousTitForTat(Strategy):
    """Class that implements the Generous Tit for Tat strategy. See the provided documentation for details.

    Args:
        chance_of_forgiveness (float): Literally the chance that the strategy forgives a defection. Note that 'chance_of_forgiveness' must be in (0, 1).
    """
    def __init__(self, chance_of_forgiveness=0.1):
        if not 0 < chance_of_forgiveness < 1:
            if chance_of_forgiveness <= 0:
                string = f"({chance_of_forgiveness} <= 0)"
            else:
                string = f"({chance_of_forgiveness} >= 1)"
            raise ValueError(f"Parameter 'chance_of_forgiveness' is out of range! " + string)
        super().__init__()
        self.chance_of_forgiveness = chance_of_forgiveness
        self.name = f"Generous Tit for Tat (p = {chance_of_forgiveness})"
        self.__doc__ = ("This is a more generous version of Tit for Tat which probabilistically forgives a defection, "
                        "as parameterized by 'chance_of_forgiveness'. Note that 'chance_of_forgiveness' must hence be"
                        " in (0, 1).")
    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history:
            return True
        if not opp_history[-1]:
            return random.random() < self.chance_of_forgiveness
        return True


