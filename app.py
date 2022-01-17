import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from sim_utils import fetch_curr, colourdict, Locations, Phases
import webbrowser
from path_utils import plotPathgeo
import numpy as np 
from network import calcPath
import pickle as pck 
import time as tm
import math

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

mapbox_access_token = open(".mapbox_token").read()

def genCircleCoords(centre, R=Phases['Visibility Radius'][0]):
    thetas = np.linspace(0,2*math.pi, 100)
    # Circumference of earth/360 =111E3 so each degree of lon/lat represents 111km
    R=R/111E3
    xs = [(centre[0] + R*math.cos(theta)) for theta in thetas]
    ys = [(centre[1] + R*math.sin(theta)) for theta in thetas]
    return xs, ys

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        # html.H4('Starlink constellation in a geographical coordinate system'),
        # html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=10000, # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))


def update_graph_live(n):
    fig = go.Figure(
                data=[go.Scattermapbox(lon=[], lat=[],
                    name="frame",
                    mode="markers",
                    marker=go.scattermapbox.Marker(size=5, color='red'))],
                layout=go.Layout(
                    xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
                    yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
                    height = 1000,
                    # width = 800,
                    # title ={
                    # 'text': "Calculating the shortest path between two locations through Starlink Phase 1",
                    # 'y':0.95,
                    # 'x':0.5,
                    # 'xanchor': 'center',
                    # 'yanchor': 'top'}
                    ))
    for phasenum in range(1,2):
        longitudes, latitudes, time = fetch_curr(phasenum)
        fig.add_trace(go.Scattermapbox(lon=longitudes, lat=latitudes,
                        name="frame",
                        mode="markers",
                        marker=go.scattermapbox.Marker(size=7.5, color=colourdict[phasenum][0])))
        for centre in zip(longitudes, latitudes):
            xs, ys = genCircleCoords(centre)
            fig.add_trace(go.Scattermapbox(
                    lon=xs,
                    lat=ys,
                    mode="lines",
                    line=dict(width=2, color='#fa8888') 
                    ))

        # plot greece locations:
        fig.add_trace(go.Scattermapbox(
                    lon=Locations['Helmos'][0],
                    lat=Locations['Helmos'][1],
                    mode="markers",
                    marker=go.scattermapbox.Marker(size=12, color='green'))) 

        fig.add_trace(go.Scattermapbox(
                    lon=Locations['Sxoinakas'][0],
                    lat=Locations['Sxoinakas'][1],
                    mode="markers",
                    marker=go.scattermapbox.Marker(size=12, color='green'))) 

        fig.add_trace(go.Scattermapbox(
                    lon=Locations['Holomondas'][0],
                    lat=Locations['Holomondas'][1],
                    mode="markers",
                    marker=go.scattermapbox.Marker(size=12, color='green')))              

        # for live dijkstra plotting when all positions have been calculated
        # if False:
        #     source = Locations['LDN']
        #     destination = Locations['SIN']
        #     fig.add_trace(go.Scattermapbox(lon=[source[0], destination[0]], lat=[source[1], destination[1]],
        #                     name="frame",
        #                     mode="markers",
        #                     marker=go.scattermapbox.Marker(size=10, color='green')))
            
        #     rtt, path, positions = calcPath(phasenum, source, destination, int(np.floor(time/10)*10))
        #     fig.add_annotation(
        #         text="Time Elapsed: "+str(time)+"s, Round Trip Time: "+str(2*np.round(rtt/300E3,3))+"ms",#, Path: "+str([str(i) for i in shortest_path[1]]),
        #         showarrow=False,
        #         yshift=-340, font=dict(size=18))
        #     fig.add_annotation(
        #         text="Path: "+str([str(i) for i in path])+', Hop count: '+str(len(path)),
        #         showarrow=False,
        #         yshift=-370, font=dict(size=18))
        #     fig = plotPathgeo(source, destination, phasenum, path, positions, fig)
        fig.update_layout(showlegend=False,  
        mapbox=dict(
            accesstoken=mapbox_access_token, 
            style='light',
            zoom=1.4))

    return fig

def begin_dash():
    if __name__ == '__main__':
        app.run_server(debug=True)
    
begin_dash()