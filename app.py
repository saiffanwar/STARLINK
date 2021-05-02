import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from geometry import fetch_curr, colourdict, Locations, Phases
import webbrowser
from dijkstra import plotPath, plotCircle
import numpy as np 
from network import calcPath, onePlot
import pickle as pck 
import time as tm


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

mapbox_access_token = open(".mapbox_token").read()



graphdict = {}
section=1
print('reading dicts')
for i in np.arange(10,1000, 10):
    graphdict[str(i)] = pck.load(open('data/'+str(int(Phases['Altitude'][section-1]/1E3))+'/'+str(i)+'.pck', 'rb'))
print('dicts read')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        # html.H4('Starlink constellation in a geographical coordinate system'),
        # html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
        )
    ])
)
# try:
#     print('Reading graphdict file....')
#     graphdict = pck.load(open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'rb'))
#     print('File opened.')
# except:
#     pck.dump([], open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'wb'))

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))

def update_graph_live(n):
    # print(n)
    # Initialise plot
    # onePlot('New York', 'London')
    fig = go.Figure(
                data=[go.Scattermapbox(lon=[], lat=[],
                    name="frame",
                    mode="markers",
                    marker=go.scattermapbox.Marker(size=5, color='red'))],
                layout=go.Layout(
                    xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
                    yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
                    height = 800,
                    width = 1600,
                    title ={
                    'text': "Calculating the shortest path between two locations through Starlink Phase 1",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'}
                    ))
    # if time!=0:
    for i in range(1,2):
        longitudes, latitudes, time = fetch_curr(i)
        fig.add_trace(go.Scattermapbox(lon=longitudes, lat=latitudes,
                        name="frame",
                        mode="markers",
                        marker=go.scattermapbox.Marker(size=5, color=colourdict[i])))

        # for live dijkstra plotting when all positions have been calculated
        source = Locations['London']
        destination = Locations['Johannesburg']
        plotCircle(Phases['max ground reach'][i], source[0], source[0])
        fig.add_trace(go.Scattermapbox(lon=[source[0], destination[0]], lat=[source[1], destination[1]],
                        name="frame",
                        mode="markers",
                        marker=go.scattermapbox.Marker(size=10, color='green')))
        shortest_path, positions = calcPath(source, destination, int(np.floor(time/10)*10), graphdict)
        # shortest_path = calcPath(source, destination, time, graphdict)

        fig.add_annotation(
            text="Time Elapsed: "+str(time)+"s, Shortest Path Latency: "+str(np.round(shortest_path[0]/300E3,3))+"ms",#, Path: "+str([str(i) for i in shortest_path[1]]),
            showarrow=False,
            yshift=-340, font=dict(size=18))
        fig.add_annotation(
            text="Path: "+str([str(i) for i in shortest_path[1]])+', Hop count: '+str(len(shortest_path[1])),
            showarrow=False,
            yshift=-370, font=dict(size=18))
        fig = plotPath(shortest_path[1], positions, fig)
        fig.update_layout(showlegend=False,  
        mapbox=dict(
            accesstoken=mapbox_access_token, 
            style='light',
            zoom=1.4))
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