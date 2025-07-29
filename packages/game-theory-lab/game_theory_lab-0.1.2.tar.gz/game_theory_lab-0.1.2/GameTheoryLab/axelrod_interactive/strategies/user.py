from GameTheoryLab.axelrod_interactive.strategy import Strategy

class User(Strategy):
    """Class that implements the User strategy - an interface through which the user can play the game!"""
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.__doc__ = (f"This is a human, going by the name of {self.name}. No one knows how this player's going to "
                        f"dole out his moves. Let's find out, shall we?")

    def move(self, opp_history, self_history, opp_score, self_score):
        print("Your turn!")

        print("Here what your opponent has played so far: ")
        print(["C" if move else "D" for move in opp_history])

        print("And here's what YOU've played so far!")
        print(["C" if move else "D" for move in self_history])

        print(f"Your current score: {self_score}")
        print(f"Your opponent's score: {opp_score}")

        print(f"Over to you, {self.name}. Let's see if you can outdo your opponent!")
        choice = input("Choose a move. Type 'C' for 'Cooperate' or 'D' for 'Defect': ").title()
        while choice not in {"C", "D"}:
            print("I said type 'C' for 'Cooperate' or 'D' for 'Defect'! C'mon, follow instructions :( ")
            choice = input("Choose a move. Type 'C' for 'Cooperate' or 'D' for 'Defect': ").title()

        return choice == "C"

