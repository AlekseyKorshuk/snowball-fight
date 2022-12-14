from dash import Dash
from dash_components import payoff_component, get_layout
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output
from dash_components import *
from agents import AllDAgent, AllCAgent, TitForTatAgent


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] + [dbc.themes.GRID]
agents = [AllDAgent, AllCAgent, TitForTatAgent]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = get_layout()
dropdown_id = 'winning_conditions_dropdown'
div_id = 'winning_conditions_display'
# app.layout = winning_conditions_dropdown(agents,
#                                          dropdown_id=dropdown_id,
#                                          div_id=div_id)
#
#
# @app.callback(
#     Output(div_id, 'children'),
#     Input(dropdown_id, 'value')
# )
# def winning_conditions_display(value):
#     conditions = utils.compute_formula(agents)[value]
#     print(type(conditions[0]))
#     return html.Div(
#         html.Div(
#             className="trend",
#             children=[
#                 html.Ul(id='my-list', children=[html.Li(i) for i in conditions])
#             ],
#         )
#     )

# app.layout = tabs_component()
# register_tabs_callback(app, tab1_component(), tab2_component())

# app.layout = get_layout()

if __name__ == '__main__':
    app.run_server(debug=True)