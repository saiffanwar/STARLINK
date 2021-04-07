import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from geometry import fetch_locs, fetch_orbit
import webbrowser

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        # html.H4('Starlink constellation in a geographical coordinate system'),
        # html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    # Create the graph with subplots
    fig = go.Figure(
                data=[go.Scattergeo(lon=[], lat=[],
                    name="frame",
                    mode="markers",
                    marker=dict(color='red', size=5))],
                layout=go.Layout(
                    xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
                    yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
                    height = 700,
                    width = 1500,
                    title ={
                    'text': "Starlink constellation in a geographical coordinate system",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'}
                    ))
    for i in range(1,6):
        longitudes, latitudes, no_of_planes, sats_per_plane, colour = fetch_locs(i)
        fig.add_trace(go.Scattergeo(lon=longitudes, lat=latitudes,
                        name="frame",
                        mode="markers",
                        marker=dict(color=colour, size=5)))
        # xs, ys = fetch_orbit()
        # fig.add_trace(go.Scattergeo(lon=xs, lat=ys,
        #                 name="frame",
        #                 mode="lines",
        #                 line=dict(width=2, color="blue")))
    return fig

# port = 8050 # or simply open on the default `8050` port

# def open_browser():
# 	webbrowser.open_new("http://localhost:{}".format(port))

def begin_dash():
    if __name__ == '__main__':
        app.run_server(debug=True)
    
begin_dash()