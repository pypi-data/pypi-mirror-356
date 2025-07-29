import json

payoffs_file_path = "GameTheoryLab/axelrod_interactive/payoffs.json"

def set_payoffs(t=5, r=3, p=1, s=0):
    """Sets the payoff matrix for the session. It MUST be called immediately after loading the library in, otherwise a payoff matrix won't exist."""
    with open(payoffs_file_path, "r") as file:
        payoff_dict = json.load(file)

    payoff_dict["Temptation"] = t
    payoff_dict["Reward"] = r
    payoff_dict["Punishment"] = p
    payoff_dict["Sucker"] = s

    with open(payoffs_file_path, "w") as file:
        json.dump(payoff_dict, file)

def get_payoffs():
    """Returns the payoff matrix for the session."""
    with open(payoffs_file_path, "r") as file:
        payoff_dict = json.load(file)

    return payoff_dict
