from GameTheoryLab.axelrod_interactive.strategy import Strategy
from GameTheoryLab.axelrod_interactive import get_payoffs
from GameTheoryLab.axelrod_interactive.result import Result

class Arena:
    payoffs = get_payoffs()
    def __init__(self, s1: Strategy, s2: Strategy, num_rounds: int=10, show_results: bool=True):
        # Validation
        if not isinstance(s1, Strategy):
            raise ValueError("Parameter 's1' is not a Strategy.")
        if not isinstance(s2, Strategy):
            raise ValueError("Parameter 's2' is not a Strategy.")
        if not isinstance(num_rounds, int):
            raise ValueError(f"Parameter 'num_rounds' must be an integer! (You entered {num_rounds}).")
        if not isinstance(show_results, bool):
            raise ValueError(f"Parameter 'show_results' must be a boolean! (You entered {show_results}).")

        self.show_results = show_results
        self.s1 = s1
        self.s2 = s2
        self.num_rounds = num_rounds
        self.s1_history = []
        self.s2_history = []
        self.s1_score = 0
        self.s2_score = 0

    def run(self):
        choice1 = self.s1.play(self.s2_history, self.s1_history, self.s2_score, self.s1_score)
        choice2 = self.s2.play(self.s1_history, self.s2_history, self.s1_score, self.s2_score)

        self.s1_history.append(choice1)
        self.s2_history.append(choice2)

        if choice1 and choice2:
            self.s1_score += self.payoffs["Reward"]
            self.s2_score += self.payoffs["Reward"]

        elif choice1:
            self.s1_score += self.payoffs["Sucker"]
            self.s2_score += self.payoffs["Temptation"]

        elif choice2:
            self.s1_score += self.payoffs["Temptation"]
            self.s2_score += self.payoffs["Sucker"]

        else:
            self.s1_score += self.payoffs["Punishment"]
            self.s2_score += self.payoffs["Punishment"]

    def play_round(self):
        """This simulates the two players going at it for the specified number of times. Who's going to win this round?"""
        self.s1.prep_for_match()
        self.s2.prep_for_match()
        for _ in range(self.num_rounds):
            if self.s1_score < 0 or self.s2_score < 0:
                break
            self.run()

        if self.show_results:
            print(f"{self.s1}'s moves: ")
            print(["C" if move else "D" for move in self.s1_history])

            print(f"{self.s2}'s moves: ")
            print(["C" if move else "D" for move in self.s2_history])

            print(f"Results: {self.s1_score} - {self.s2_score}")
            print("\n")

        result_dict = {"Move": list(range(1, self.num_rounds + 1)) + ["SCORE"],
                       self.s1.name: ["C" if move else "D" for move in self.s1_history] + [self.s1_score],
                       self.s2.name: ["C" if move else "D" for move in self.s2_history] + [self.s2_score]}
        return Result(result_dict)
