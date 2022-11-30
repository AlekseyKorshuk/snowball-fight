import math
from snowball_fight.agents.base import BaseAgent


class AllDAgent(BaseAgent):

    @BaseAgent.on_step
    def shoot_to_opponent_field(self, opponent_last_shot_to_your_field, snowball_number,
                                minutes_passed_after_your_shot) -> int:
        if (minutes_passed_after_your_shot % 4 == 0 and minutes_passed_after_your_shot != 0) or self.current_step == 60:
            return min(
                snowball_number,
                self.current_step_available_shooting_balls
            )
        return 0

    @BaseAgent.on_step
    def shoot_to_hot_field(self, opponent_last_shot_to_your_field, snowball_number,
                           minutes_passed_after_your_shot) -> int:
        return 0


if __name__ == '__main__':
    agent = AllCAgent()

    print(agent.shoot_to_opponent_field(123, 0, 0))
    print(agent.shoot_to_hot_field(123, 0, 0))
    print(agent)

    assert agent.current_step == 1
    assert agent.current_step_available_shooting_balls == 0
    assert agent.shooting_method_was_called_in_this_round is False
    assert agent.opponent_shots == [123]
