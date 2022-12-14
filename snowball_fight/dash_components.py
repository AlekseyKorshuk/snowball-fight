import utils
from agents import AllDAgent, AllCAgent, TitForTatAgent
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc, html
import dash_daq as daq
from dash import dash_table, html, dcc, Output, Input


def payoff_component():
    agents = [AllDAgent, AllCAgent, TitForTatAgent]
    agent_names = [agent.__name__ for agent in agents]
    payoff_matrix = utils.get_payoff_matrix(agents)
    payoff_dataframe = pd.DataFrame(payoff_matrix, columns=agent_names, index=agent_names)
    df = payoff_dataframe.reset_index()
    df.rename(columns={"index": ''}, inplace=True)
    return [
        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    ]


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
                        style={'margin-left': '3%', 'margin-right': '3%', 'margin-top': '1%', 'margin-bottom': '1%'},
                        width=3
                    ),
                    dbc.Col(
                        [
                            html.H4('Payoff Matrix', style={'textAlign': 'center'}),
                            # table
                            html.Div(id='payoff-table', children=payoff_component()),
                            # formula
                            # html.Div(id='formula'),
                        ],
                        width=8

                    )
                ]
            )
        ]

    )


def tp_component(agents):
    tp = utils.get_total_payoff_vector(agents)
    tp = list(map(str, tp))

    return html.Div(
        html.Div(
            className="trend",
            children=[
                html.Ul(id='my-list', children=[html.Li(i) for i in tp])
            ],
        )
    )


def winning_conditions_dropdown(agents):
    agent_names = [agent.__name__ for agent in agents]

    return html.Div([
        dcc.Dropdown(agent_names, agent_names[0], id='winning_conditions_dropdown'),
        html.Div(id='winning_conditions_display')
    ])


def register_winning_conditions_callback(app, agents):
    @app.callback(
        Output('winning_conditions_display', 'children'),
        Input('winning_conditions_dropdown', 'value')
    )
    def winning_conditions_display(value):
        conditions = utils.compute_formula(agents)[value]
        print(type(conditions[0]))
        return html.Div(
            html.Div(
                className="trend",
                children=[
                    html.Ul(id='my-list', children=[html.Li(i) for i in conditions])
                ],
            )
        )


def tabs_component():
    return html.Div([
        dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
            dcc.Tab(label='Tab one', value='tab-1'),
            dcc.Tab(label='Tab two', value='tab-2'),
        ]),
        html.Div(id='tabs-example-content-1')
    ])


def register_tabs_callback(app, tab1, tab2):
    @app.callback(
        Output('tabs-example-content-1', 'children'),
        Input('tabs-example-1', 'value')
    )
    def render_content(tab):
        if tab == 'tab-1':
            return tab1
        elif tab == 'tab-2':
            return tab2


def tab1_component():
    return html.Div([
        html.H3('Tab content 1'),
        dcc.Graph(
            figure=dict(
                data=[dict(
                    x=[1, 2, 3],
                    y=[3, 1, 2],
                    type='bar'
                )]
            )
        )
    ])


def tab2_component():
    return html.Div([
        html.H3('Tab content 2'),
        dcc.Graph(
            figure=dict(
                data=[dict(
                    x=[1, 2, 3],
                    y=[5, 10, 6],
                    type='bar'
                )]
            )
        )
    ])


