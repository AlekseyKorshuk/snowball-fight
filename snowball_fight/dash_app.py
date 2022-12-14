
from dash import Dash
from dash_components import payoff_component


app = Dash(__name__)

app.layout = payoff_component()

if __name__ == '__main__':
    app.run_server(debug=True)