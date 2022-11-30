import math


def max_snowballs_per_minute(minutes_passed_after_your_shot):
    exp = math.exp(minutes_passed_after_your_shot)
    return int(15 * exp / (15 + exp))


class BaseAgent:

    def __init__(self):
        self.current_step_available_shooting_balls = 0
        self.current_step = 0
        self.shooting_method_was_called_in_this_round = False
        self.opponent_shots = list()

    def reset(self):
        self.current_step_available_shooting_balls = 0
        self.current_step = 0
        self.shooting_method_was_called_in_this_round = False
        self.opponent_shots = list()

    def on_step(method):
        def inner(self, opponent_last_shot_to_your_field, snowball_number, minutes_passed_after_your_shot):
            if not self.shooting_method_was_called_in_this_round:
                self.current_step += 1
                self.current_step_available_shooting_balls = max_snowballs_per_minute(
                    minutes_passed_after_your_shot
                )
                self.update_opponent_shots(opponent_last_shot_to_your_field)

            self.shooting_method_was_called_in_this_round = not self.shooting_method_was_called_in_this_round
            num_balls = method(self, opponent_last_shot_to_your_field, snowball_number, minutes_passed_after_your_shot)
            self.current_step_available_shooting_balls -= num_balls
            return num_balls
        return inner

    def update_opponent_shots(self, opponent_last_shot_to_your_field):
        self.opponent_shots.append(opponent_last_shot_to_your_field)

    @on_step
    def shoot_to_opponent_field(self, opponent_last_shot_to_your_field, snowball_number,
                                minutes_passed_after_your_shot) -> int:
        raise NotImplementedError

    @on_step
    def shoot_to_hot_field(self, opponent_last_shot_to_your_field, snowball_number,
                           minutes_passed_after_your_shot) -> int:
        raise NotImplementedError

    def __str__(self):
        return dict(
            class_name=self.__class__.__name__,
            current_step_available_shooting_balls=self.current_step_available_shooting_balls,
            current_step=self.current_step,
            shooting_method_was_called_in_this_round=self.shooting_method_was_called_in_this_round,
            opponent_shots=self.opponent_shots
        ).__str__()


if __name__ == '__main__':
    agent = BaseAgent()

    try:
        agent.shoot_to_opponent_field(123, 0, 0)
    except NotImplementedError:
        pass

    try:
        agent.shoot_to_hot_field(123, 0, 0)
    except NotImplementedError:
        pass

    assert agent.current_step == 1
    assert agent.current_step_available_shooting_balls == 0
    assert agent.shooting_method_was_called_in_this_round is False
    assert agent.opponent_shots == [123]
