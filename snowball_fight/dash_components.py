import utils
from agents import *
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
from dash import dcc, html
import dash_daq as daq
from dash import dash_table, html, dcc, Output, Input, State
import sympy as sp

from snowball_fight.playground.game_loop import agents_to_leaderboard_default


def payoff_component(agents):
    # agents = utils.get_filtered_agents()

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


def get_input_list():
    all_agents = utils.get_all_possible_agents()
    all_agents_names = [agent.__name__ for agent in all_agents]

    css_style1 = {
        "position": "relative",
        "display": "flex",
        "flex-wrap": "wrap",
        "align-items": "stretch",
        "width": "100%",
    }
    # '''
    css_style = {
        "display": "flex",
        "align-items": "center",
        "padding": ".375rem .75rem",
        "font-size": "1rem",
        "font-weight": "400",
        "line-height": "1.5",
        "color": "#212529",
        "text-align": "center",
        "white-space": "nowrap",
        "background-color": "#e9ecef",
        "border": "1px solid  #ced4da",
        "border-radius": ".25rem",
    }
    # '''
    rows = [
        dbc.InputGroup(
            [
                dbc.InputGroupText(agent, style=css_style),
                dbc.Input(placeholder="Amount", type="number", value=1, min=0, step=1),
            ],
            className="mb-3",
            style=css_style1
        ) for agent in all_agents_names
    ]

    return html.Div(rows, id='agent-leaderboard-table-body')


def register_agents_toggle_callback(app):
    @app.callback(
        Output('payoff-table', 'children'),
        Output('total-payoff-dropdown', 'children'),
        Output('win-conditions-dropdown', 'children'),
        Input('compute-button', 'n_clicks'),
        State('agent-table-body', 'children')
    )
    def helper(_, value):
        on_value = lambda x: x['props']['children'][1]['props']['children']['props']['on']
        filter_values = list(map(on_value, value))

        filtered_agents = utils.get_filtered_agents(filter_values)

        return payoff_component(filtered_agents), \
               winning_conditions_dropdown(filtered_agents), \
               winning_conditions_dropdown(filtered_agents)


def register_leaderboard_callback(app):
    @app.callback(
        Output('leaderboard-table', 'children'),
        Input('compute-leaderboard-button', 'n_clicks'),
        State('agent-leaderboard-table-body', 'children')
    )
    def helper(_, value):
        num_occurences = []
        for row in value:
            num_occurences.append(int(row['props']['children'][1]['props']['value']))

        return leaderboard_component(utils.get_all_possible_agents(), num_players=num_occurences)


def get_layout():
    return html.Div(
        [
            html.H1('Snowball Fight Dashboard', style={'textAlign': 'center'}),
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Formulas', value='tab-1'),
                dcc.Tab(label='Leaderboard', value='tab-2'),
            ]),
            html.Div(id='tabs-content'),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Footer(
                [
                    dcc.Markdown(
                        "**Created by [Aleksey Korshuk](https://github.com/AlekseyKorshuk), [Viacheslav Sinii](https://github.com/ummagumm-a), [Timur Aizatvafin](https://github.com/timuraiz)**"),
                    dcc.Markdown(
                        "[![GitHub stars](https://img.shields.io/github/stars/AlekseyKorshuk/snowball-fight?style=social)](https://github.com/AlekseyKorshuk/snowball-fight)"
                    ),
                ],
                style={'display': 'inline-block', 'width': '100%', 'text-align': 'center'}
            ),
            html.Br(),
            html.Br(),
            html.Br(),
        ]
    )


def get_tab_1_layout():
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.H4('Agents', style={'textAlign': 'left', 'margin-right': '3%'}),
                    html.Div(get_toggle_list(), style={'textAlign': 'center', "overflow": "scroll", "max-height": "500px"}),
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
                    html.Div(id='payoff-table', children=payoff_component(utils.get_all_possible_agents())),
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
                    html.H4('Agents', style={'textAlign': 'left', 'margin-right': '3%'}),
                    html.Div(get_input_list()),
                    html.Br(),
                    html.Button('Compute', id='compute-leaderboard-button', style={'textAlign': 'center'}),
                ],
                style={'margin-left': '3%', 'margin-right': '3%', 'margin-top': '1%', 'margin-bottom': '1%'},
                width=3
            ),
            dbc.Col(
                [
                    html.H4('Leaderboard', style={'textAlign': 'center'}),
                    # table
                    html.Div(id='leaderboard-table', children=leaderboard_component(utils.get_all_possible_agents())),
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
        selected_value = value['props']['children'][0]['props']['value']
        possible_answers = value['props']['children'][0]['props']['options']

        agents = list(map(eval, possible_answers))

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
        agents = value['props']['children'][0]['props']['options']
        agents = list(map(eval, agents))
        formula = utils.compute_formula(agents)
        answers = formula[selected_value]
        if len(answers) == 1 and str(answers[0]) == 'True':
            string_latext = sp.latex(sp.Symbol("Always wins"))
        else:
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
        dcc.Dropdown(agent_names, agent_names[0]),
        html.Div(id='winning_conditions_display')
    ])


def register_winning_conditions_callback(app, agents):
    @app.callback(
        Output('winning_conditions_display', 'children'),
        Input('winning_conditions_dropdown', 'value')
    )
    def winning_conditions_display(value):
        agents = value['props']['children'][0]['props']['options']
        agents = list(map(eval, agents))
        conditions = utils.compute_formula(agents)[value]
        return html.Div(
            html.Div(
                className="trend",
                children=[
                    html.Ul(id='my-list', children=[html.Li(i) for i in conditions])
                ],
            )
        )


def leaderboard_component(agents, **kwargs):
    leaderboard = agents_to_leaderboard_default(agents, **kwargs)

    df = pd.DataFrame(leaderboard, columns=['Agent', 'Score'])
    return [
        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    ]
