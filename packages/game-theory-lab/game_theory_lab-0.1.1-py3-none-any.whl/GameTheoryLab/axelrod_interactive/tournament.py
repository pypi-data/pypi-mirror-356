from GameTheoryLab.axelrod_interactive.result import Result
from GameTheoryLab.axelrod_interactive.strategy import Strategy
from GameTheoryLab.axelrod_interactive.arena import Arena

class Tournament:
    def __init__(self, strategies: list[Strategy], mode: str="round robin", num_repeats: int=5, num_rounds: int=200):
        """Simulates a tournament with the given strategies.

           Args:
              strategies (list[Strategy]): the strategies to compete in the tournament. Number of strategies must be at least 3.
              mode (str): the mode of tournament to play. Currently supports three modes: 'round robin', 'four ways' and 'round of 16'. If 'round robin' is chosen, any number of strategies can be passed in. If 'four ways' is chosen, the number of strategies passed in must be exactly 4. If 'round of 16' is chosen, the number of strategies must be exactly 16. The default mode is 'round robin'.
              num_repeats (int): Number of times a single tournament is repeated. Defaults to 5.
              num_rounds (int): Number of rounds per match between any two strategies. Defaults to 200.
           """
        # Validation
        if len(strategies) < 3:
            raise ValueError(f"Strategies list is too small! ({len(strategies)} < 3)")
        if mode not in {"round of 16", "round robin", "four ways"}:
            raise ValueError(f"Mode {mode} either doesn't exist or is not supported.")
        if mode == "four ways" and len(strategies) != 4:
            raise ValueError(f"Mode {mode} requires exactly 4 strategies (but you passed in {len(strategies)}).")
        if mode == "round of 16" and len(strategies) != 16:
            raise ValueError(f"Mode {mode} requires exactly 16 strategies (but you passed in {len(strategies)}).")
        if not isinstance(num_rounds, int):
            raise ValueError(f"Parameter 'num_rounds' must be an integer! (You entered {num_rounds}.)")
        if not isinstance(num_repeats, int):
            raise ValueError(f"Parameter 'num_repeats' must be an integer! (You entered {num_repeats}.)")

        self.base_strategies = strategies
        self.strategies = strategies

        self.round_robin_results = {}
        self.num_players = len(self.strategies)
        self.mode = mode

        self.base_num_repeats = num_repeats
        self.num_repeats = self.base_num_repeats

        self.base_num_rounds = num_rounds
        self.num_rounds = self.base_num_rounds

    def __reset(self):
        self.strategies = self.base_strategies
        self.round_robin_results = {}
        self.num_players = len(self.strategies)
        self.num_repeats = self.base_num_repeats
        self.num_rounds = self.base_num_rounds

    def show_info(self):
        string = ""
        if self.mode == "round robin":
            string = f"Round robin ({self.num_rounds} rounds per match, {self.num_repeats} repetitions)"
        elif self.mode == "round of 16":
            string = "Round of 16"
        elif self.mode == "four ways":
            string = "Four ways"

        print("Mode:", string)
        print("Players:")
        for i in range(len(self.strategies)):
            print(f"{i + 1}:", self.strategies[i].name)

    def __play_round_robin(self, show_results=True):
        for _ in range(self.num_repeats):
            for i in range(self.num_players):
                for j in range(i, self.num_players):
                    player1 = self.strategies[i]
                    player2 = self.strategies[j]
                    arena = Arena(player1, player2, num_rounds=self.num_rounds, show_results=False)
                    result_dict = arena.play_round().data
                    p1_score, p2_score = result_dict[player1.name][-1], result_dict[player2.name][-1]
                    self.round_robin_results[player1.name] = self.round_robin_results.get(player1.name, 0) + p1_score
                    self.round_robin_results[player2.name] = self.round_robin_results.get(player2.name, 0) + p2_score
        for player in self.strategies:
            self.round_robin_results[player.name] /= (self.num_players * self.num_repeats)

        self.strategies.sort(key=lambda x: self.round_robin_results[x.name], reverse=True)
        winner = self.strategies[0].name

        if show_results:
            print(f"The winner is: {winner}!")
            print("Results: \n")

            for s in self.strategies:
                print(f"{s.name}: {round(self.round_robin_results[s.name], 2)}")

        leaderboard = {(name := self.strategies[i].name): (i + 1, self.round_robin_results[name]) for i in range(self.num_players)}
        results_dict = {
            "Rank": [],
            "Player": [],
            "Score": []
        }
        for player in leaderboard:
            results_dict["Rank"].append(leaderboard[player][0])
            results_dict["Player"].append(player)
            results_dict["Score"].append(leaderboard[player][1])
        return Result(results_dict)

    def __play_four_ways(self, show_results=True):
        if show_results:
            print("--------------------------------SEMI-FINALS----------------------------------")
        string = "Players: "
        for strategy in self.strategies:
            string += strategy.name + ", "
        print(string.strip(", ") + "\n")

        for i in range(4):
            for j in range(i + 1, 4):
                player1 = self.strategies[i]
                player2 = self.strategies[j]
                arena = Arena(player1, player2, num_rounds=self.num_rounds, show_results=False)
                result_dict = arena.play_round().data
                p1_score, p2_score = result_dict[player1.name][-1], result_dict[player2.name][-1]
                self.round_robin_results[player1.name] = self.round_robin_results.get(player1.name, 0) + p1_score
                self.round_robin_results[player2.name] = self.round_robin_results.get(player2.name, 0) + p2_score
        for player in self.strategies:
            self.round_robin_results[player.name] /= self.num_players
        self.strategies.sort(key=lambda x: self.round_robin_results[x.name], reverse=True)

        if show_results:
            print("----------------------------------FINALS---------------------------------------")
        finalist1, finalist2 = self.strategies[:2]
        finals = Arena(finalist1, finalist2, num_rounds=self.num_rounds, show_results=show_results)
        result_dict = finals.play_round().data
        f1_score, f2_score = result_dict[finalist1.name][-1], result_dict[finalist2.name][-1]
        if f1_score > f2_score:
            print(f"The winner is: {finalist1.name}!")
        elif f1_score < f2_score:
            print(f"The winner is: {finalist2.name}")
        else:
            print("Tie!")

    def __play_round_of_16(self, show_results=True):
        results = {
            "Player": [],
            "Reached Quarter Finals": [],
            "Reached Semi Finals": [],
            "Reached Finals": [],
            "Won?": []
        }
        table = {player.name: [False] * 4 for player in self.strategies}
        # ------------------------------------------------------R16--------------------------------------------------
        for i in range(16):
            for j in range(i + 1, 16):
                player1 = self.strategies[i]
                player2 = self.strategies[j]
                arena = Arena(player1, player2, num_rounds=self.num_rounds, show_results=False)
                result_dict = arena.play_round().data
                p1_score, p2_score = result_dict[player1.name][-1], result_dict[player2.name][-1]
                self.round_robin_results[player1.name] = self.round_robin_results.get(player1.name, 0) + p1_score
                self.round_robin_results[player2.name] = self.round_robin_results.get(player2.name, 0) + p2_score
        for player in self.strategies:
            self.round_robin_results[player.name] /= self.num_players
        self.strategies.sort(key=lambda x: self.round_robin_results[x.name], reverse=True)

        for i in range(16):
            if i < 8:
                table[self.strategies[i].name][0] = True
            else:
                table[self.strategies[i].name][0] = False

        # ------------------------------------------------------Quarter Finals----------------------------------------
        for i in range(8):
            for j in range(i + 1, 8):
                player1 = self.strategies[i]
                player2 = self.strategies[j]
                arena = Arena(player1, player2, num_rounds=self.num_rounds, show_results=False)
                result_dict = arena.play_round().data
                p1_score, p2_score = result_dict[player1.name][-1], result_dict[player2.name][-1]
                self.round_robin_results[player1.name] = self.round_robin_results.get(player1.name, 0) + p1_score
                self.round_robin_results[player2.name] = self.round_robin_results.get(player2.name, 0) + p2_score
        for player in self.strategies:
            self.round_robin_results[player.name] /= self.num_players
        self.strategies.sort(key=lambda x: self.round_robin_results[x.name], reverse=True)

        for i in range(8):
            if i < 4:
                table[self.strategies[i].name][1] = True
            else:
                table[self.strategies[i].name][1] = False

        # -------------------------------------------------------Semi Finals------------------------------------------

        for i in range(4):
            for j in range(i + 1, 4):
                player1 = self.strategies[i]
                player2 = self.strategies[j]
                arena = Arena(player1, player2, num_rounds=self.num_rounds, show_results=False)
                result_dict = arena.play_round().data
                p1_score, p2_score = result_dict[player1.name][-1], result_dict[player2.name][-1]
                self.round_robin_results[player1.name] = self.round_robin_results.get(player1.name, 0) + p1_score
                self.round_robin_results[player2.name] = self.round_robin_results.get(player2.name, 0) + p2_score
        for player in self.strategies:
            self.round_robin_results[player.name] /= self.num_players
        self.strategies.sort(key=lambda x: self.round_robin_results[x.name], reverse=True)

        for i in range(4):
            if i < 2:
                table[self.strategies[i].name][2] = True
            else:
                table[self.strategies[i].name][2] = False

        # -------------------------------------------------------Finals------------------------------------------
        if show_results:
            print("----------------------------------FINALS---------------------------------------")

        finalist1, finalist2 = self.strategies[:2]
        finals = Arena(finalist1, finalist2, num_rounds=self.num_rounds, show_results=show_results)
        result_dict = finals.play_round().data
        f1_score, f2_score = result_dict[finalist1.name][-1], result_dict[finalist2.name][-1]
        if f1_score > f2_score:
            print(f"The winner is: {finalist1.name}!")
            table[self.strategies[0].name][3] = True
            table[self.strategies[1].name][3] = False
        elif f1_score < f2_score:
            print(f"The winner is: {finalist2.name}")
            table[self.strategies[1].name][3] = True
            table[self.strategies[0].name][3] = False
        else:
            print("Tie!")
            table[self.strategies[0].name][3] = False
            table[self.strategies[1].name][3] = False

        for player in self.strategies:
            results["Player"].append(player.name)
            results["Reached Quarter Finals"].append(table[player.name][0])
            results["Reached Semi Finals"].append(table[player.name][1])
            results["Reached Finals"].append(table[player.name][2])
            results["Won?"].append(table[player.name][3])

        return Result(results)

    def play(self, show_results):
        self.__reset()
        self.show_info()
        if self.mode == "round robin":
            return self.__play_round_robin(show_results=show_results)
        elif self.mode == "four ways":
            return self.__play_four_ways(show_results=show_results)
        elif self.mode == "round of 16":
            return self.__play_round_of_16(show_results=show_results)

