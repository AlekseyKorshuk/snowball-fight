import math
from .base import BaseAgent


class Spiteful(BaseAgent):
    '''
    Cooperates until the opponent defects and thereafter always defects
    '''

    def __init__(self):
        super().__init__()
        self.is_attacked = False

    def reset(self):
        super(Spiteful, self).reset()
        self.is_attacked = False

    @BaseAgent.on_step
    def shoot_to_opponent_field(self, opponent_last_shot_to_your_field, snowball_number,
                                minutes_passed_after_your_shot) -> int:
        if not self.is_attacked:
            self.is_attacked = self.get_opponent_shots_sum(4) > 0
        if self.is_attacked:
            if (minutes_passed_after_your_shot % 4 == 0 and minutes_passed_after_your_shot != 0) \
                    or self.current_step == self.total_steps:
                return min(
                    snowball_number,
                    self.current_step_available_shooting_balls
                )
        return 0

    @BaseAgent.on_step
    def shoot_to_hot_field(self, opponent_last_shot_to_your_field, snowball_number,
                           minutes_passed_after_your_shot) -> int:
        if not self.is_attacked:
            self.is_attacked = self.get_opponent_shots_sum(4) > 0
        if not self.is_attacked:
            if (minutes_passed_after_your_shot % 4 == 0 and minutes_passed_after_your_shot != 0) \
                    or self.current_step == self.total_steps:
                return min(
                    snowball_number,
                    self.current_step_available_shooting_balls
                )
        return 0
