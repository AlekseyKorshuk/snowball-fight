def on_step(method):
    def inner(agent_instance, opponent_last_shot_to_your_field, snowball_number, minutes_passed_after_your_shot):
        method(agent_instance, opponent_last_shot_to_your_field, snowball_number, minutes_passed_after_your_shot)

    return inner


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

    @on_step
    def shoot_to_opponent_field(self, opponent_last_shot_to_your_field, snowball_number,
                                minutes_passed_after_your_shot):
        raise NotImplementedError

    @on_step
    def shoot_to_hot_field(self, opponent_last_shot_to_your_field, snowball_number, minutes_passed_after_your_shot):
        raise NotImplementedError
