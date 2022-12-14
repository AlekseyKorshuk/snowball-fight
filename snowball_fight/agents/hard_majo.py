import math
from base import BaseAgent


class HardMojo(BaseAgent):
    '''
    Defects on the first move and defects if the number of defections of the opponent is greater than or equal to the
    number of times she has cooperated. Else she cooperates
    '''

    def __init__(self):
        super().__init__()
        self.first_move_is_done = False
        self.opponent_hits = 0
        self.mojo_cooperation = 0

    def reset(self):
        super(HardMojo, self).reset()
        self.first_move_is_done = False
        self.opponent_hits = 0
        self.mojo_cooperation = 0

    @BaseAgent.on_step
    def shoot_to_opponent_field(self, opponent_last_shot_to_your_field, snowball_number,
                                minutes_passed_after_your_shot) -> int:

        is_attacked = self.get_opponent_shots_sum(4) > 0
        if is_attacked:
            self.opponent_hits += 1
        if not self.first_move_is_done or self.opponent_hits >= self.mojo_cooperation:
            if not self.first_move_is_done:
                self.first_move_is_done = True
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

        is_attacked = self.get_opponent_shots_sum(4) > 0
        if not is_attacked or (is_attacked and self.mojo_cooperation >= self.opponent_hits):
            if not is_attacked:
                self.mojo_cooperation += 1
            if (minutes_passed_after_your_shot % 4 == 0 and minutes_passed_after_your_shot != 0) \
                    or self.current_step == self.total_steps:
                return min(
                    snowball_number,
                    self.current_step_available_shooting_balls
                )
        return 0


if __name__ == '__main__':
    agent = HardMojo()

    print(agent.shoot_to_opponent_field(123, 0, 0))
    print(agent.shoot_to_hot_field(123, 0, 0))
    print(agent)

    assert agent.current_step == 1
    assert agent.current_step_available_shooting_balls == 0
    assert agent.shooting_method_was_called_in_this_round is False
    assert agent.opponent_shots == [123]
