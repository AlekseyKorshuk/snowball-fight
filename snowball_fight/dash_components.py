import utils
from agents import AllDAgent, AllCAgent, TitForTatAgent
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table


def payoff_component():
    agents = [AllDAgent, AllCAgent, TitForTatAgent]
    agent_names = [agent.__name__ for agent in agents]
    payoff_matrix = utils.get_payoff_matrix(agents)
    payoff_dataframe = pd.DataFrame(payoff_matrix, columns=agent_names, index=agent_names)
    df = payoff_dataframe.reset_index()
    df.rename(columns={"index": ''}, inplace=True)
    # tp = utils.get_total_payoff_vector(agents, payoff_matrix)
    # print(tp)
    # tp_dataframe = pd.DataFrame([tp], index=agent_names)
    # print(df)

    return dbc.Container([
        dbc.Label('Click a cell in the table:'),
        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]),
        dbc.Alert(id='tbl_out'),
    ])