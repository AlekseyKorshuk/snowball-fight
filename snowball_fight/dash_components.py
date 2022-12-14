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
    return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])


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
        [
            html.H1('Snowball Fight Dashboard', style={'textAlign': 'center'}),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4('Agents', style={'textAlign': 'left', 'margin-right': '3%'}),
                            html.Div(table_body, style={'textAlign': 'center'}),
                            html.Br(),
                            html.Button('Compute', id='compute-button', style={'textAlign': 'center'}),
                        ],
                        style={'margin-left': '3%', 'margin-right': '3%', 'margin-top': '1%', 'margin-bottom': '1%',
                               'width': '30%'},
                    ),
                    dbc.Col(
                        [
                            html.H4('Payoff Matrix', style={'textAlign': 'center'}),
                            # table
                            html.Div(id='payoff-table', children=list(payoff_component())),
                            # formula
                            # html.Div(id='formula'),
                        ],
                        style={'margin-left': '3%', 'margin-right': '3%', 'margin-top': '1%', 'margin-bottom': '1%',
                               'width': '70%'},
                        width=6

                    )
                ]
            )
        ]

    )
