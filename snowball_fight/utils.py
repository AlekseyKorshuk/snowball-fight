import sympy as sp

from snowball_fight.playground.game_loop import game_loop
from snowball_fight.agents.all_c import AllCAgent
from snowball_fight.agents.all_d import AllDAgent
from snowball_fight.agents.tit_for_tat import TitForTatAgent


def get_payoff(agent1, agent2):
    payoff1, payoff2 = game_loop(agent1, agent2)
    print(f'{agent1.__class__.__name__} vs {agent2.__class__.__name__}: {payoff1} vs {payoff2}')
    return payoff1, payoff2


def compute_formula(agent_classes):
    formula = None
    # get pairs without repetitions
    for i in range(len(agent_classes)):
        for j in range(i + 1, len(agent_classes)):
            agent1 = agent_classes[i]()
            agent2 = agent_classes[j]()
            payoff1, payoff2 = get_payoff(agent1, agent2)
            if formula is None:
                formula = sp.sympify(
                    f'{payoff1} * {agent1.__class__.__name__} + {payoff2} * {agent2.__class__.__name__}')
            else:
                formula += sp.sympify(
                    f'{payoff1} * {agent1.__class__.__name__} + {payoff2} * {agent2.__class__.__name__}')

    return formula


if __name__ == '__main__':
    agent_classes = [
        AllCAgent,
        AllCAgent,
        # AllDAgent,
        # TitForTatAgent,
    ]
    formula = compute_formula(agent_classes)
    print(formula)

'''
AllCAgent vs AllDAgent: 220 vs 58
AllCAgent vs TitForTatAgent: 58 vs 58
AllDAgent vs TitForTatAgent: 209 vs 220

inequality:
AllCAgent*58 + AllDAgent*220 <= AllDAgent*209 + AllCAgent*58 + AllCAgent*58 + AllDAgent*220
AllDAgent*220 + AllCAgent*58 < AllDAgent*209 + AllCAgent*58
'''
