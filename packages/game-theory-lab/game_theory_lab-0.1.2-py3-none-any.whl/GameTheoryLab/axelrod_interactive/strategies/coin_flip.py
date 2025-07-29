import random
from GameTheoryLab.axelrod_interactive.strategy import Strategy

class CoinFlip(Strategy):
    """Class that implements the 'coin flip' (aka random) strategy.

    Args:
        prob_of_cooperation (float): The probability that the strategy cooperates for any given round. Defaults to 0.5.
    """
    def __init__(self, prob_of_cooperation=0.5):
        # Validation
        if not 0 < prob_of_cooperation < 1:
            if prob_of_cooperation <= 0:
                string = f"({prob_of_cooperation} <= 0)"
            else:
                string = f"({prob_of_cooperation} >= 1)"
            raise ValueError(f"Parameter 'prob_of_cooperation' is out of range! " + string)

        super().__init__()
        self.prob_of_cooperation = prob_of_cooperation

        self.name = f"Coin Flip (p = {self.prob_of_cooperation})"
        self.__doc__ = "This strategy randomly cooperates or defects at any given moment in the game."

    def move(self, opp_history, self_history, opp_score, self_score):
        return random.random() < self.prob_of_cooperation
