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
register_agents_toggle_callback(app)

# dropdown_id = 'winning_conditions_dropdown'
# div_id = 'winning_conditions_display'
# app.layout = winning_conditions_dropdown(agents)
# register_winning_conditions_callback(app, agents)


# app.layout = tabs_component()
# register_tabs_callback(app, tab1_component(), tab2_component())
register_total_payoff_callback(app, agents)
register_win_conditions_callback(app, agents)

# app.layout = get_layout()

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
