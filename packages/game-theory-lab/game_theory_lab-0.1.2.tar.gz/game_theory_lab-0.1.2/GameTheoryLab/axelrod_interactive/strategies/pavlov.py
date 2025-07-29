from GameTheoryLab.axelrod_interactive.strategy import Strategy

class Pavlov(Strategy):
    """Class that implements the Pavlov strategy. See the provided documentation for details."""
    def __init__(self):
        super().__init__()
        self.name = "Pavlov"
        self.__doc__ = ("Also known as 'Win-Stay-Lose-Shift', this strategy starts by cooperating, and from then on, "
                        "he repeats his last play if it won him the last round, and changes play otherwise.")

    def move(self, opp_history, self_history, opp_score, self_score):
        # Neat, isn't it?
        return not opp_history or opp_history[-1]