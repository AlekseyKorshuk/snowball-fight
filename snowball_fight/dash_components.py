import utils
from agents import AllDAgent, AllCAgent, TitForTatAgent
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc, html
import dash_daq as daq
from dash import dash_table, html, dcc, Output, Input, State
import sympy as sp


def payoff_component(filter_agents=None):
    agents = utils.get_all_possible_agents()
    if filter_agents is not None:
        agents = [agent for (agent, flag) in zip(agents, filter_agents) if flag]

    agent_names = [agent.__name__ for agent in agents]
    payoff_matrix = utils.get_payoff_matrix(agents)
    payoff_dataframe = pd.DataFrame(payoff_matrix, columns=agent_names, index=agent_names)
    df = payoff_dataframe.reset_index()
    df.rename(columns={"index": ''}, inplace=True)
    return [
        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    ]


def get_toggle_list():
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

    return table_body


def register_agents_toggle_callback(app):
    @app.callback(
        Output('payoff-table', 'children'),
        Input('compute-button', 'n_clicks'),
        State('agent-table-body', 'children')
    )
    def helper(_, value):
        on_value = lambda x: x['props']['children'][1]['props']['children']['props']['on']
        filter_values = list(map(on_value, value))

        return payoff_component(filter_values)


def get_layout():
    return html.Div(
        [
            html.H1('Snowball Fight Dashboard', style={'textAlign': 'center'}),
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Formulas', value='tab-1'),
                dcc.Tab(label='Leaderboard', value='tab-2'),
            ]),
            html.Div(id='tabs-content')
        ]
    )


def get_tab_1_layout():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H4('Agents', style={'textAlign': 'left', 'margin-right': '3%'}),
                    html.Div(get_toggle_list(), style={'textAlign': 'center'}),
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
                    html.H4('Total Payoff Formula', style={'textAlign': 'center'}),
                    html.Div(id='total-payoff-dropdown',
                             children=winning_conditions_dropdown(utils.get_all_possible_agents())),
                    html.Div(id='total-payoff-formula', children=[]),
                    # win conditions
                    html.H4('Win Conditions', style={'textAlign': 'center'}),
                    html.Div(id='win-conditions-dropdown',
                             children=winning_conditions_dropdown(utils.get_all_possible_agents())),
                    html.Div(id='win-conditions-answer', children=[]),
                ],
                width=8

            )
        ]
    )


def get_tab_2_layout():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H4('TEST', style={'textAlign': 'left', 'margin-right': '3%'}),
                    html.Div(get_toggle_list(), style={'textAlign': 'center'}),
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
                    html.H4('Total Payoff Formula', style={'textAlign': 'center'}),
                    html.Div(id='total-payoff-dropdown',
                             children=winning_conditions_dropdown(utils.get_all_possible_agents())),
                    html.Div(id='total-payoff-formula', children=[]),
                    # win conditions
                    html.H4('Win Conditions', style={'textAlign': 'center'}),
                    html.Div(id='win-conditions-dropdown',
                             children=winning_conditions_dropdown(utils.get_all_possible_agents())),
                    html.Div(id='win-conditions-answer', children=[]),
                ],
                width=8

            )
        ]
    )


def register_tab_callback(app, agents):
    @app.callback(Output('tabs-content', 'children'),
                  Input('tabs', 'value'))
    def render_content(tab):
        if tab == 'tab-1':
            return get_tab_1_layout()
        elif tab == 'tab-2':
            return get_tab_2_layout()


def register_total_payoff_callback(app, agents):
    @app.callback(
        Output('total-payoff-formula', 'children'),
        Input('total-payoff-dropdown', 'n_clicks'),
        State('total-payoff-dropdown', 'children')
    )
    def helper(_, value):
        print(value)
        selected_value = value['props']['children'][0]['props']['value']
        possible_answers = value['props']['children'][0]['props']['options']
        tp = utils.get_total_payoff_vector(agents)
        tp = tp[possible_answers.index(selected_value)]

        return html.H6(
            [
                dcc.Markdown(sp.latex(tp, mode='inline'), mathjax=True)
            ],
            style={'textAlign': 'center'}
        )


def register_win_conditions_callback(app, agents):
    @app.callback(
        Output('win-conditions-answer', 'children'),
        Input('win-conditions-dropdown', 'n_clicks'),
        State('win-conditions-dropdown', 'children')
    )
    def helper(_, value):
        selected_value = value['props']['children'][0]['props']['value']
        formula = utils.compute_formula(agents)
        answers = formula[selected_value]
        string_latext = "$\\begin{cases}"
        for answer in answers:
            string_latext += sp.latex(answer.simplify()) + ' \\\ '
        string_latext += "\end{cases}$"
        return html.H6(
            [
                dcc.Markdown(string_latext, mathjax=True)
            ],
            style={'textAlign': 'center'}
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
