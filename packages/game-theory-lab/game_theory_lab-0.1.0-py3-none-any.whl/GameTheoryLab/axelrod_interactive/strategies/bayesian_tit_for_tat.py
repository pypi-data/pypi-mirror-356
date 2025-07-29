from GameTheoryLab.axelrod_interactive import get_payoffs
from GameTheoryLab.axelrod_interactive.strategy import Strategy
import random

class BayesianTitForTat(Strategy):
    """
    Class that implements the Bayesian Tit for Tat strategy. See provided documentation for details.

    Args:
        Note that all parameters apart from 'confidence' must be in (0, 1).
        p_cooperator (float): Perceived probability that opponent mostly cooperates. Defaults to 1/3.
        p_defector (float): Perceived probability that opponent mostly defects. Defaults to 1/3.
        trust (float): Perceived chance that opponent would defect, given that the opponent is believed to be a 'cooperator'. Defaults to 0.1.
        suspicion (float): Perceived chance that opponent would defect, given that the opponent is believed to be a 'defector'. Defaults to 0.9.
        randomness (float): Perceived chance that opponent would defect, given that the opponent is believed to be playing randomly. Defaults to 0.5.
        confidence (int): Number of consistent plays by the opponent before deciding against randomness. Defaults to 5.
        delta_r (float): The extent to which the belief that opponent is playing randomly is reduced, once confidence is reached. Defaults to 0.5.
    """
    payoffs = get_payoffs()
    def __init__(self, p_cooperator=1/3, p_defector=1/3, trust=0.9, suspicion=0.9, randomness=0.5, confidence=5, delta_r=0.5):
        # Validation
        if not 0 < p_cooperator < 1:
            if p_cooperator <= 0:
                string = f"{p_cooperator} <= 0"
            else:
                string = f"{p_cooperator} >= 1"
            raise ValueError(f"Parameter 'p_cooperator' is out of range! ({string})")

        if not 0 < p_defector < 1:
            if p_defector <= 0:
                string = f"{p_defector} <= 0"
            else:
                string = f"{p_defector} >= 1"
            raise ValueError(f"Parameter 'p_defector' is out of range! ({string})")

        if not 0 < trust < 1:
            if trust <= 0:
                string = f"{trust} <= 0"
            else:
                string = f"{trust} >= 1"
            raise ValueError(f"Parameter 'trust' is out of range! ({string})")

        if not 0 < suspicion < 1:
            if suspicion <= 0:
                string = f"{suspicion} <= 0"
            else:
                string = f"{suspicion} >= 1"
            raise ValueError(f"Parameter 'suspicion' is out of range! ({string})")

        if not 0 < randomness < 1:
            if randomness <= 0:
                string = f"{randomness} <= 0"
            else:
                string = f"{randomness} >= 1"
            raise ValueError(f"Parameter 'randomness' is out of range! ({string})")

        if not 0 < delta_r < 1:
            if delta_r <= 0:
                string = f"{delta_r} <= 0"
            else:
                string = f"{delta_r} >= 1"
            raise ValueError(f"Parameter 'delta_r' is out of range! ({string})")

        super().__init__()
        self.name = "Bayesian Tit for Tat"

        self.base_pc = p_cooperator
        self.p_cooperator = p_cooperator

        self.base_pd = p_defector
        self.p_defector = p_defector

        base_pr = 1 - self.p_defector - self.p_cooperator
        self.base_pr = base_pr
        self.p_random = 1 - self.p_defector - self.p_cooperator

        self.base_trust = trust
        self.trust = trust

        self.base_suspicion = suspicion
        self.suspicion = suspicion

        self.base_randomness = randomness
        self.randomness = randomness

        self.confidence = confidence

        self.base_dr = delta_r
        self.delta_r = delta_r
        self.__doc__ = """This strategy uses Bayesian inference to determine the behaviour of the opponent, 
        as determined using the parameters, and responds accordingly.
        
        Using Bayes' Theorem, the strategy's belief of the opponent's cooperation, defection, or randomness is 
        calculated as follows. Denote P(C) by the probability that the opponent is a 'cooperator', i.e. one that 
        mostly cooperates, and similarly define P(D) and P(R). Let P(C|D) be the probability that the opponent 
        cooperates given that the opponent is a defector; define P(D|C), P(C|C), P(D|D), P(C|R), P(D|R) similarly.
        - If the opponent cooperates: 
          Let N = P(C)P(D|C) + P(D)P(D|D) + P(R)P(D|R); then 
          P(C) -> P(C)P(D|C)/N, 
          P(D) -> P(D)P(D|D)/N, and 
          P(R) -> P(R)P(D|R)/N. 
        - If the opponent defects: 
          Let N = P(C)P(C|C) + P(D)P(C|D) + P(R)P(C|R); then 
          P(C) -> P(C)P(C|C)/N, 
          P(D) -> P(D)P(C|D)/N, and 
          P(R) -> P(R)P(C|R)/N."""

    def additional_prep(self):
        self.p_cooperator = self.base_pc
        self.p_defector = self.base_pd
        self.p_random = self.base_pr
        self.trust = self.base_trust
        self.suspicion = self.base_suspicion
        self.randomness = self.base_randomness
        self.delta_r = self.base_dr

    def update_history(self, opp_history, self_history):
        if self_history:
            confidence_interval = opp_history[-self.confidence:]
            if confidence_interval.count(False) == self.confidence:
                self.randomness *= self.delta_r

            elif 0.4 < confidence_interval.count(False) / self.confidence < 0.6:
                self.randomness /= self.delta_r

            if opp_history[-1]:
                self.p_cooperator *= self.trust
                self.p_defector *= (1 - self.suspicion)
                self.p_random *= self.randomness
            else:
                self.p_cooperator *= (1 - self.trust)
                self.p_defector *= self.suspicion
                self.p_random *= (1 - self.randomness)

            norm = self.p_cooperator + self.p_defector + self.p_random
            self.p_cooperator /= norm
            self.p_defector /= norm
            self.p_random /= norm

    def move(self, opp_history, self_history, opp_score, self_score):
        if not opp_history:
            return True

        return random.random() < self.p_cooperator




