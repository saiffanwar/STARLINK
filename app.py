import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from geometry import *
import webbrowser
from dijkstra import *
import networkx as nx
import numpy as np 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        # html.H4('Starlink constellation in a geographical coordinate system'),
        # html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1000/5, # in milliseconds
            n_intervals=0
        )
    ])
)
section=1
with open('data/graphdict'+str(int(Phases['Altitude'][section-1]/1E3))+'.pck', 'rb') as f:
    graphdict = pck.load(f)
# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    # print(n)
    # Create the graph with subplots
    fig = go.Figure(
                data=[go.Scattergeo(lon=[], lat=[],
                    name="frame",
                    mode="markers",
                    marker=dict(color='red', size=5))],
                layout=go.Layout(
                    xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
                    yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
                    height = 1000,
                    width = 2250,
                    title ={
                    'text': "Calculating the shortest path between two locations through a satellite constellation",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'}
                    ))
    # if time!=0:
    for i in range(1,2):
        longitudes, latitudes, time = fetch_curr(i)
        fig.add_trace(go.Scattergeo(lon=longitudes, lat=latitudes,
                        name="frame",
                        mode="markers",
                        marker=dict(color=colourdict[i][0], size=5)))

        # for live dijkstra plotting when all positions have been calculated
    # for i in range(1,2):
    #     longitudes, latitudes = fetch_locs(i,time)
    #     fig.add_trace(go.Scattergeo(lon=longitudes, lat=latitudes,
    #                     name="frame",
    #                     mode="markers",
    #                     marker=dict(color=colourdict[i][0], size=5)))
    # if (time)%10 == 0:
    # try:
        G, positions = graphdict[str(int(np.floor(time/10)*10))]

        source = Locations['New York']
        destination = Locations['London']
        source_sat = find_sat(source, positions)
        destination_sat = find_sat(destination, positions)

        shortest_path = nx.single_source_dijkstra(G, source_sat, destination_sat, weight='weight')
        fig.add_annotation(
            text="Shortest Path Latency: "+str(np.round(shortest_path[0]/300E3,3))+"ms",
            showarrow=False,
            yshift=-300)
        fig = plot(shortest_path[1], positions, fig)
        fig.update_layout(showlegend=False)
    # except:
    #     pass

    return fig

# port = 8050 # or simply open on the default `8050` port

# def open_browser():
# 	webbrowser.open_new("http://localhost:{}".format(port))

def begin_dash():
    if __name__ == '__main__':
        app.run_server(debug=True)
    
begin_dash()