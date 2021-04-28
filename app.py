import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from geometry import fetch_curr, colourdict, Locations, Phases
import webbrowser
from dijkstra import plotPath
import numpy as np 
from network import calcPath
import pickle as pck 

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
try:
    print('Reading graphdict file....')
    graphdict = pck.load(open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'rb'))
    print('File opened.')
except:
    pck.dump([], open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'wb'))

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))

def update_graph_live(n):
    # print(n)
    # Initialise plot
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
        source = Locations['New York']
        destination = Locations['London']
        shortest_path, positions = calcPath(source, destination, int(np.floor(time/10)*10), graphdict)
        # shortest_path = calcPath(source, destination, time, graphdict)

        fig.add_annotation(
            text="Shortest Path Latency: "+str(np.round(shortest_path[0]/300E3,3))+"ms",
            showarrow=False,
            yshift=-300)
        fig = plotPath(shortest_path[1], positions, fig)
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