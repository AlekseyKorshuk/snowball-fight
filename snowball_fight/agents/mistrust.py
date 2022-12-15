import math
from base import BaseAgent


class Mistrust(BaseAgent):
    '''
    Defects on the first move then play what my opponent played the previous move
    '''

    def __init__(self):
        super().__init__()
        self.first_step_past = False

    def reset(self):
        super(Mistrust, self).reset()
        self.first_step_past = False

    @BaseAgent.on_step
    def shoot_to_opponent_field(self, opponent_last_shot_to_your_field, snowball_number,
                                minutes_passed_after_your_shot) -> int:
        if (minutes_passed_after_your_shot % 4 == 0 and minutes_passed_after_your_shot != 0) \
                or self.current_step == self.total_steps:
            is_attacked = self.get_opponent_shots_sum(4) > 0
            if not self.first_step_past or is_attacked:
                if not self.first_step_past:
                    self.first_step_past = True
                return min(
                    snowball_number,
                    self.current_step_available_shooting_balls
                )
        return 0

    @BaseAgent.on_step
    def shoot_to_hot_field(self, opponent_last_shot_to_your_field, snowball_number,
                           minutes_passed_after_your_shot) -> int:
        if (minutes_passed_after_your_shot % 4 == 0 and minutes_passed_after_your_shot != 0) \
                or self.current_step == self.total_steps:
            is_attacked = self.get_opponent_shots_sum(4) > 0
            if not is_attacked and self.first_step_past:
                return min(
                    snowball_number,
                    self.current_step_available_shooting_balls
                )
        return 0


if __name__ == '__main__':
    agent = Mistrust()

    print(agent.shoot_to_opponent_field(123, 0, 0))
    print(agent.shoot_to_hot_field(123, 0, 0))
    print(agent)

    assert agent.current_step == 1
    assert agent.current_step_available_shooting_balls == 0
    assert agent.shooting_method_was_called_in_this_round is False
    assert agent.opponent_shots == [123]
