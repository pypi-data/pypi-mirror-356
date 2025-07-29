import random

from Cython.Build.Dependencies import default_create_extension

from GameTheoryLab.axelrod_interactive.strategy import Strategy

class GrimAttacker(Strategy):
    """Class that implements the Grim Attacker strategy. See the provided documentation for details.

    Args:
        defect_streak (int): The number of times opponent defects in a row before conclusively being identified as the grim trigger. Defaults to 3.
        coop_streak (int): The number of times for which the strategy initially cooperates before defecting to test for Grim Trigger's behavior. Defaults to 2.
    """
    def __init__(self, defect_streak: int=3, coop_streak: int=2):
        # Validation
        if not isinstance(defect_streak, int):
            raise ValueError(f"Parameter 'defect_streak' must be an integer! (You entered {defect_streak})")
        if not isinstance(coop_streak, int):
            raise ValueError(f"Parameter 'coop_streak' must be an integer! (You entered {coop_streak})")

        super().__init__()
        self.opp_is_grim = None

        self.base_cs = coop_streak
        self.coop_streak = coop_streak

        self.base_ds = defect_streak
        self.defect_streak = self.base_ds

        self.prob_of_cooperation = 0.15

        self.name = "Grim Attacker"
        self.__doc__ = """This strategy has one mission: to beat Grim Trigger in the round robin tournament. The 
        strategy starts off by cooperating 'coop_streak' times, then defecting once and then cooperating again 
        'defect_streak' times, while observing the opponent's behavior.
        
        If the opponent defects throughout the testing period, the strategy concludes that the opponent is the Grim 
        Trigger, and then defects for the remainder of the round. Otherwise, and if he defects unexpectedly (such as 
        while no defects have been made), the strategy concludes he is NOT the Grim Trigger, and he proceeds to 
        mirror GTFT's strategy with a 0.15 chance of forgiveness."""

    def additional_prep(self):
        self.defect_streak = self.base_ds
        self.coop_streak = self.base_cs
        self.opp_is_grim = None

    def update_history(self, opp_history, self_history):
        if self.opp_is_grim is not None: return

        if opp_history:
            if not opp_history[-1]:
                if self.coop_streak > -1:
                    self.opp_is_grim = False
                elif self.defect_streak == 0 and self.opp_is_grim is None:
                    self.opp_is_grim = True
            else:
                if not self_history[-1]:
                    return
                if self.coop_streak == -1 and self.defect_streak > 0:
                    self.opp_is_grim = False



    def move(self, opp_history, self_history, opp_score, self_score):
        if self.opp_is_grim is None:
            while self.coop_streak > 0:
                self.coop_streak -= 1
                return True

            if self.coop_streak == 0:
                self.coop_streak -= 1
                return False

            while self.defect_streak > 0:
                self.defect_streak -= 1
                return True

        else:
            if self.opp_is_grim:
                return False

            elif not opp_history[-1]:
                return random.random() < self.prob_of_cooperation

            return True
