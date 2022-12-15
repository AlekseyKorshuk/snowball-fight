# Snowball Figth

We created a tool for analyzing the performance of agents in the snowball fight game. Implemented automatic calculations of the number of agents of each type present such that a specific agent always wins. Our project allows contributors to easily extend agent ZOO and analyze performance and simulate games.

# Quick Start

Use the Dash application out of the box to evaluate existing players and simulate the game.

## Installation

Execute the following commands to install:

```bash
git clone https://github.com/AlekseyKorshuk/snowball-fight
cd snowball-fight
pip install -e .
```

## Dash Application

To evaluate agents and simulate the game, use Dash:

```bash
python3 snowball_fight/dash_app.py
```

<p float="left">
<img width="1512" alt="Screenshot 2022-12-15 at 16 34 59" src="https://user-images.githubusercontent.com/48794610/207872446-e09c2c20-480b-4698-bc73-9f576778553c.png">
<img width="1512" alt="Screenshot 2022-12-15 at 16 35 42" src="https://user-images.githubusercontent.com/48794610/207872572-37701c2a-99c6-46b7-829b-90fb17f3f9fb.png">
</p>

# How to add agents

You can easily add your custom agent in a few steps:

1. Create a new file with the following path `snowball_fight/agents/NAMEAgent.py`
2. Use BaseAgent as a parent class:
```python
from snowball_fight.agents.base import BaseAgent


class NAMEAgent(BaseAgent):

    @BaseAgent.on_step
    def shoot_to_opponent_field(self, opponent_last_shot_to_your_field, snowball_number,
                                minutes_passed_after_your_shot) -> int:
        return 0

    @BaseAgent.on_step
    def shoot_to_hot_field(self, opponent_last_shot_to_your_field, snowball_number,
                           minutes_passed_after_your_shot) -> int:
        return 0
```
3. Base class already has such features as current step, list of previous actions by both players, etc. 

# Acknowledgement

This project is based on the second assignment of the Game Theory course at Innopolis University and presented by [Aleksey Korshuk](https://github.com/AlekseyKorshuk), [Viacheslav Sinii](https://github.com/ummagumm-a) and [Timur Aizatvafin](https://github.com/timuraiz) during Colloquium.

[![GitHub stars](https://img.shields.io/github/stars/AlekseyKorshuk/snowball-fight?style=social)](https://github.com/AlekseyKorshuk/snowball-fight)
