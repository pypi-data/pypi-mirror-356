from .settings import PAYOFFS

payoff_dict = PAYOFFS.copy()
def set_payoffs(t=5, r=3, p=1, s=0):
    """Sets the payoff matrix for the session. It MUST be called immediately after loading the library in, otherwise a payoff matrix won't exist."""
    payoff_dict["Temptation"] = t
    payoff_dict["Reward"] = r
    payoff_dict["Punishment"] = p
    payoff_dict["Sucker"] = s

def get_payoffs():
    """Returns the payoff matrix for the session."""
    return payoff_dict
