import math
from .base import BaseAgent


class TitForTatAgent(BaseAgent):
    '''
    Cooperates the two first moves, then defects only if the opponent has defected during the two previous moves
    '''

    def __init__(self, total_steps=60):
        super().__init__(total_steps=total_steps)
        self.first_steps = [4, 8]

    @BaseAgent.on_step
    def shoot_to_opponent_field(self, opponent_last_shot_to_your_field, snowball_number,
                                minutes_passed_after_your_shot) -> int:

        if (minutes_passed_after_your_shot % 4 == 0 and minutes_passed_after_your_shot != 0) \
                or self.current_step == self.total_steps:
            if self.current_step not in self.first_steps:
                is_attacked = self.get_opponent_shots_sum(4) > 0
                if is_attacked:
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
            if self.current_step in self.first_steps or not is_attacked:
                return min(
                    snowball_number,
                    self.current_step_available_shooting_balls
                )
        return 0


if __name__ == '__main__':
    agent = TitForTatAgent()

    print(agent.shoot_to_opponent_field(123, 0, 0))
    print(agent.shoot_to_hot_field(123, 0, 0))
    print(agent)

    assert agent.current_step == 1
    assert agent.current_step_available_shooting_balls == 0
    assert agent.shooting_method_was_called_in_this_round is False
    assert agent.opponent_shots == [123]
