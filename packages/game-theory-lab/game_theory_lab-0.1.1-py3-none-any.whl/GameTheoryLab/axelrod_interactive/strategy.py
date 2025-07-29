from abc import ABC, abstractmethod

class Strategy(ABC):
    """The base class that is inherited by all concrete strategy classes."""
    name: str
    prob_of_cooperation: float
    prob_of_defection: float
    opps_defect_count: int
    self_defect_count: int
    opps_coop_count: int
    self_coop_count: int

    def __init__(self):
        pass

    def __repr__(self):
        return self.name

    def additional_prep(self):
        pass

    def prep_for_match(self):
        self.opps_defect_count = 0
        self.self_defect_count = 0
        self.opps_coop_count = 0
        self.self_coop_count = 0
        self.additional_prep()

    def update_history(self, opp_history, self_history):
        if self_history:
            if self_history[-1]:
                self.self_coop_count += 1
            else:
                self.self_defect_count += 1

            if opp_history[-1]:
                self.opps_coop_count += 1
            else:
                self.opps_defect_count += 1

    def play(self, opp_history, self_history, opp_score, self_score):
        self.update_history(opp_history, self_history)
        return self.move(opp_history, self_history, opp_score, self_score)

    @abstractmethod
    def move(self, opp_history, self_history, opp_score, self_score):
        pass


