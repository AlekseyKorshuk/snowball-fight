import utils
from agents import AllDAgent, AllCAgent, TitForTatAgent
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc, html
import dash_daq as daq


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


def get_layout():
    all_agents = utils.get_all_possible_agents()
    all_agents_names = [agent.__name__ for agent in all_agents]

    rows = [
        html.Tr([html.Td(agent), html.Td(
            daq.BooleanSwitch(
                id='agent-' + agent,
                on=True,
            )
        )]) for agent in all_agents_names
    ]

    table_body = [html.Tbody(rows, id='agent-table-body')]

    return html.Div(
        html.Div([
            html.H4('Snowball Fight Dashboard', style={'textAlign': 'center'}),
            html.Div(table_body, style={'textAlign': 'center'}),
            # html.Br(),
            # html.Div([
            #     "⠀Library (optional): ",
            #     dcc.Input(id='gym_lib', value="", type='text')
            # ], style={'textAlign': 'center'}),
            # html.H5(id='live-update-text', style={'textAlign': 'center'}),
            # dcc.Graph(id='live-update-graph'),
            # html.Div([
            # ], style={'textAlign': 'center'}, id="videos"),
            # dcc.Interval(
            #     id='interval-component',
            #     interval=1 * 1000,  # in milliseconds
            #     n_intervals=0
            # ),
            # html.Div(id='placeholder', children="placeholder", style={'display': 'none'})
        ])
    )
