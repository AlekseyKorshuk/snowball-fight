from dash import Dash
from dash_components import payoff_component, get_layout

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = get_layout()

if __name__ == '__main__':
    app.run_server(debug=True)
