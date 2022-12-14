import sympy as sp
import numpy as np
from snowball_fight.playground.game_loop import game_loop
from snowball_fight.agents.all_c import AllCAgent
from snowball_fight.agents.all_d import AllDAgent
from snowball_fight.agents.tit_for_tat import TitForTatAgent
from snowball_fight.agents import ALL_AGENTS
import re


def get_payoff(agent1, agent2):
    payoff1, payoff2 = game_loop(agent1, agent2)
    # print(f"Payoff for {agent1.__class__.__name__} vs {agent2.__class__.__name__}: {payoff1} vs {payoff2}")
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


def get_total_payoff_vector(agent_classes, payoff_matrix=None):
    if payoff_matrix is None:
        payoff_matrix = get_payoff_matrix(agent_classes)
    n_matrix = sp.Matrix([[agent_class.__name__] for agent_class in agent_classes])
    diagonal_matrix = sp.Matrix(np.diagonal(payoff_matrix))
    payoff_matrix = sp.Matrix(payoff_matrix)
    diagonal_matrix = sp.diag(diagonal_matrix)
    vector_tp = payoff_matrix * n_matrix - diagonal_matrix
    return vector_tp


def postprocess_constraints(constraints):
    print(constraints)
    return constraints


def compute_formula(agent_classes, is_zero_possible=True):
    win_rules = dict()
    payoff_matrix = get_payoff_matrix(agent_classes)
    vector_tp = get_total_payoff_vector(agent_classes, payoff_matrix)

    for i in range(len(agent_classes)):
        win_rules[agent_classes[i].__name__] = []
        for j in range(len(agent_classes)):
            if i != j:
                equation = sp.sympify(f"{vector_tp[i]} - {vector_tp[j]} <= 0")
                equation = equation.simplify()
                # check if the equation is already in the list
                exists = False
                for eq_ in win_rules[agent_classes[i].__name__]:
                    if str(equation) == str(eq_):
                        exists = True
                        break
                if not exists:
                    win_rules[agent_classes[i].__name__].append(equation)
        for agent in agent_classes:
            value = ">" if agent.__name__ == agent_classes[i].__name__ or not is_zero_possible else ">="
            print(f"{agent.__name__} {value} 0")
            win_rules[agent_classes[i].__name__].append(sp.sympify(f"{agent.__name__} {value} 0"))

        print(f"Before reduction {agent_classes[i].__name__}: ", win_rules[agent_classes[i].__name__])
        reduced = None
        for agent in agent_classes:
            try:
                symbols = [sp.Symbol(agent.__name__)]
                result = post_process(
                    sp.reduce_inequalities(win_rules[agent_classes[i].__name__],
                                           symbols=symbols),
                    agent_classes
                )
                if (reduced is not None and len(result) < len(reduced)) or reduced is None:
                    reduced = result
                # print(f"Done for {agent_classes[i].__name__} with {agent.__name__}")
                break
            except Exception as ex:
                pass

        if reduced is not None:
            # print(f"Reduced for {agent_classes[i].__name__}: {reduced}")
            win_rules[agent_classes[i].__name__] = reduced

        # print(win_rules[agent_classes[i].__name__])
        # win_rules[agent_classes[i].__name__] = set(win_rules[agent_classes[i].__name__])

    return win_rules


def post_process(system_solution, agent_classes):
    if system_solution is None or system_solution == sp.false:
        return system_solution
    system_solution = str(system_solution)
    system_solution = re.sub(r'\(\w+ < oo\)', '', system_solution)
    system_solution = re.sub(r'\(\w+ > -oo\)', '', system_solution)
    system_solution = re.sub(r'\(-oo < \w+\)', '', system_solution)

    for agent_class in agent_classes:
        agent_class_name = agent_class.__name__
        system_solution = re.sub(fr'\({agent_class_name} >= 0\)', '', system_solution)
        system_solution = re.sub(fr'\(0 <= {agent_class_name}\)', '', system_solution)
    # remove double spaces
    system_solution = re.sub(r'\s+', ' ', system_solution)
    # remove double " &"
    while ' & & ' in system_solution:
        system_solution = system_solution.replace(' & & ', ' & ')
    system_solution = re.sub(r' & &', ' &', system_solution)
    if system_solution.startswith(' &'):
        start_index = system_solution.find(f"(")
        system_solution = system_solution[start_index:]
    if system_solution.endswith('& '):
        system_solution = system_solution[:-2]

    rows = system_solution.split(' & ')
    rows = [row.strip() for row in rows]
    rows = [sp.sympify(row) for row in rows]
    # print(rows)
    return rows


def get_all_possible_agents():
    return ALL_AGENTS


def get_filtered_agents(filter_list):
    agents = [agent for (agent, flag) in zip(ALL_AGENTS, filter_list) if flag]

    return agents


if __name__ == '__main__':
    # agent_classes = [
    #     AllCAgent,
    #     AllDAgent,
    #     TitForTatAgent,
    # ]
    # formula = compute_formula(agent_classes)
    # for agent_class in agent_classes:
    #     print("#" * 20, agent_class.__name__, "#" * 20)
    #     for rule in formula[agent_class.__name__]:
    #         print(f"\t{rule}")

    # rows = [
    #     "Mistrust <= 0", "Mistrust <= -AllDAgent / 46",
    #     "Mistrust <= -25 * Pavlov / 81 - 149 * Spiteful / 243 - 25 * TitForTatAgent / 81 + 160 / 243",
    #     "Mistrust <= -46 * HardMojo / 81 - 149 * Pavlov / 243 - 46 * SoftMojo / 81 - 149 * Spiteful / 243 - 149 * TitForTatAgent / 243 + 160 / 243"
    # ]

    rows = [
        "AllDAgent >= 9 * Mistrust", "AllDAgent >= 46 * Mistrust", "AllDAgent >= 79 * Mistrust",
        "AllDAgent >= 169 * Mistrust / 2 + 75 * Pavlov / 2 + 149 * Spiteful / 2 + 75 * TitForTatAgent / 2 - 80",
        "AllDAgent >= 69 * HardMojo + 169 * Mistrust / 2 + 149 * Pavlov / 2 + 69 * SoftMojo + 149 * Spiteful / 2 + 149 * TitForTatAgent / 2 - 80"
    ]
    rows = [
        "AllDAgent >=0", "AllDAgent > 0"
    ]
    rows = [sp.sympify(row) for row in rows]

    symbols = [sp.Symbol("AllDAgent")]
    result = sp.reduce_inequalities(rows,
                                    symbols=symbols),

    # print(result)
