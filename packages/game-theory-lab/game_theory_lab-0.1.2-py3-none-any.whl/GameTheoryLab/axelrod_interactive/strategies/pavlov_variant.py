from GameTheoryLab.axelrod_interactive.strategy import Strategy

class PavlovVariant(Strategy):
    """Class that implements the Pavlov (Variant) strategy. See the provided documentation for details."""
    def __init__(self):
        super().__init__()
        self.name = "Pavlov (Variant)"
        self.__doc__ = ("Similar to Pavlov, Pavlov (Variant) switches or stays at a move based on his position in the "
                        "game. This time, Pavlov (variant) switches exactly when he's losing, and stays otherwise.")

    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history:
            return True
        return (not self_history[-1]) == self_score < opp_score


