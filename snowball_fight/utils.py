import sympy as sp
import numpy as np
from snowball_fight.playground.game_loop import game_loop
from snowball_fight.agents.all_c import AllCAgent
from snowball_fight.agents.all_d import AllDAgent
from snowball_fight.agents.tit_for_tat import TitForTatAgent


def get_payoff(agent1, agent2):
    payoff1, payoff2 = game_loop(agent1, agent2)
    # print(f'{agent1.__class__.__name__} vs {agent2.__class__.__name__}: {payoff1} vs {payoff2}')
    return payoff1, payoff2


def get_payoff_matrix(agent_classes):
    # get pairs without repetitions
    payoff_matrix = [[0 for _ in range(len(agent_classes))] for _ in range(len(agent_classes))]
    for i in range(len(agent_classes)):
        for j in range(i, len(agent_classes)):
            agent1 = agent_classes[i]()
            agent2 = agent_classes[j]()
            payoff1, payoff2 = get_payoff(agent1, agent2)
            payoff_matrix[i][j] = payoff1  # if payoff1 != 0 else 1
            payoff_matrix[j][i] = payoff2  # if payoff2 != 0 else 1

    return payoff_matrix


def compute_formula(agent_classes):
    payoff_matrix = get_payoff_matrix(agent_classes)
    n_matrix = sp.Matrix([[agent_classe.__name__] for agent_classe in agent_classes])
    diagonal_matrix = sp.Matrix(np.diagonal(payoff_matrix))
    payoff_matrix = sp.Matrix(payoff_matrix)
    diagonal_matrix = sp.diag(diagonal_matrix)
    vector_tp = payoff_matrix * n_matrix - diagonal_matrix
    # make system of equations
    agent_systems = []
    for i in range(len(agent_classes)):
        equations = []
        for j in range(len(agent_classes)):
            if i != j:
                equation = sp.sympify(f"{vector_tp[i]} < {vector_tp[j]}")
                equations.append(
                    equation
                )

        for agent_class in agent_classes:
            if agent_class != agent_classes[i]:
                equations.append(sp.sympify(f"{agent_class.__name__} >= 0"))
        print("[")
        for equation in equations:
            print('sp.sympify("', equation, '"),')
        print("]")
        # print(
        #     [
        #         sp.Symbol(agent_classes[i].__name__)
        #     ]
        # )
        system_solution = None
        try:
            system_solution = sp.reduce_inequalities(
                equations,
                symbols=[
                    sp.Symbol(agent_classes[0].__name__)
                ]
            )
        except:
            pass
        print(f"Solutions for {agent_classes[i].__name__}: {system_solution}")
        print()


if __name__ == '__main__':
    agent_classes = [
        AllCAgent,
        # AllCAgent,
        AllDAgent,
        TitForTatAgent,
    ]
    formula = compute_formula(agent_classes)
    # print(formula)
    # formula = sp.sympify(
    #     "(D - 1) * 160 + C * 1 + T * 149 > D * 160 + (C - 1) * 1 + T * 1"
    # )
    # print(formula)
    # print(formula.simplify())
    # [[-2*AllDAgent + 149*TitForTatAgent - 160 > 0, -2*AllDAgent > 0]]
    # system = [
    #     sp.sympify("(AllD - 1) * 160 + AllC * 1 + AllT * 149 > AllD * 160 + (AllC - 1) * 1 + AllT * 1"),
    #     sp.sympify("AllD * 149 + AllC * 1 + (AllT - 1) * 1 >= AllD * 160 + (AllC - 1) * 1 + AllT * 1"),
    #     sp.sympify("AllD >= 0"),
    #     sp.sympify("AllC >= 0"),
    #     sp.sympify("AllT >= 0"),
    # ]
    system = [
        # sp.sympify(
        #     "AllCAgent + 158*AllDAgent + TitForTatAgent - 1 > AllCAgent + 160*AllDAgent + 149*TitForTatAgent - 160"),
        # sp.sympify(" AllCAgent + 158*AllDAgent + TitForTatAgent - 1 > AllCAgent + 160*AllDAgent + TitForTatAgent - 1"),
        sp.sympify(" AllCAgent + 74*TitForTatAgent < 159/2 "),
        # sp.sympify(" AllDAgent < 0 "),
        sp.sympify("AllCAgent >= 0"),
        sp.sympify("AllDAgent >= 0"),
        sp.sympify("TitForTatAgent >= 0"),
    ]
    answer = sp.reduce_inequalities(
        system,
        symbols=[sp.Symbol("AllCAgent")]
    )
    # print(answer)

'''
AllCAgent vs AllDAgent: 220 vs 58
AllCAgent vs TitForTatAgent: 58 vs 58
AllDAgent vs TitForTatAgent: 209 vs 220

inequality:
AllCAgent*58 + AllDAgent*220 <= AllDAgent*209 + AllCAgent*58 + AllCAgent*58 + AllDAgent*220
AllDAgent*220 + AllCAgent*58 < AllDAgent*209 + AllCAgent*58


158*AllDAgent > 160*AllDAgent
'''
