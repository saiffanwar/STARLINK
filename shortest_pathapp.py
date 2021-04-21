import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from geometry import fetch_locs, fetch_orbit
import webbrowser
from dijkstra import *
import networkx as nx


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
    # print(n)
    # Create the graph with subplots
    fig = go.Figure(go.Scatter( 
                        x=[],y=[],
                        ))
    with open('graphdict.pck', 'rb') as f:
        graphdict = pck.load(f)
    # for i in range(100):
    networkdf = graphdict[str(n*10)]
    G = networkdf[0]
    planedfs = networkdf[1]
    print(planedfs)
    shortest_path = nx.single_source_dijkstra(G, 0,23,weight='weight')
    print('Shortest Path Latency: ', shortest_path[0]/300E6)
    fig = plot(shortest_path, planedfs, fig)
    return fig

# port = 8050 # or simply open on the default `8050` port

# def open_browser():
# 	webbrowser.open_new("http://localhost:{}".format(port))

def begin_dash():
    if __name__ == '__main__':
        app.run_server(debug=True)
    
begin_dash()