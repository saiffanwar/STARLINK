import numpy as np
from geometry import Phases, colourdict
from pprint import pprint
from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle as pck
import math

earth_radius = 6.37E6

def chunks(lst,n):
    for i in range(0, len(lst), n):
            yield lst[i:i + n]


def find_neighbours(planeNumber, satNumber, longitudes):
    sats_per_plane = len(longitudes[0])
    no_of_planes = len(longitudes)
    edges = []
    if satNumber == 0:
        edges.append([planeNumber, sats_per_plane-1])
        edges.append([planeNumber, satNumber + 1])
    elif satNumber == sats_per_plane-1:
        edges.append([planeNumber, 0])
        edges.append([planeNumber, satNumber - 1])
    else:
        edges.append([planeNumber, satNumber - 1])
        edges.append([planeNumber, satNumber + 1])

    if planeNumber == 0:
        edges.append([no_of_planes-1,satNumber])
        edges.append([planeNumber + 1,satNumber])
    elif planeNumber == no_of_planes-1:
        edges.append([0,satNumber])
        edges.append([planeNumber - 1,satNumber])
    else:
        edges.append([planeNumber - 1, satNumber])
        edges.append([planeNumber + 1, satNumber])
    networkxnodes = [(i[0]*sats_per_plane)+i[1] for i in edges]
    return edges, networkxnodes
    

# Realigns the ground map of satellites so that the starting satellite is in the centre.
# This means the furthest we can possibly travel is at the edge of the 2d map and removes need for cycling later on.
# This also halves the time complexity because we know which side of the map the destination is located

def realignment(longitude, source_sat):
    new_lon = longitude - source_sat[0]
    if new_lon < -180:
        new_lon = 180 + (new_lon%-180)
    return new_lon

# Returns the distance between 2 satellites in km.
# Distance between deg of longitude is 111.32km.
# Distance between deg of latitude is 111km.
def calcDistanceBetween(source_loc, dest_loc):
    # distance = np.sqrt((((source_loc[0] - dest_loc[0])*111.32E3)**2)+(((source_loc[1] - dest_loc[1])*111E3)**2))
    # distance = np.linalg.norm([source_loc, dest_loc])
    distance = np.sqrt((source_loc[0] - dest_loc[0])**2+(source_loc[1] - dest_loc[1])**2+(source_loc[2] - dest_loc[2])**2)
    return distance


def drawEdges(section, sat1, planedfs, fig):
    planeNumber, satNumber = sat1
    satAttributes = planedfs[str(section)].iloc[planeNumber][satNumber]
    print(planedfs[str(section)].iloc[planeNumber][satNumber]['Neighbours'])
    

def plotPath(shortest_path, positions, fig=None, all_edges=None):
    if not fig:
        fig = go.Figure(go.Scattermapbox( 
                        lon=[],lat=[],
                        ))
    for section in range(1,2):
        no_of_planes = Phases['Planes'][section-1]
        sats_per_plane = Phases['Sats per plane'][section-1]
        colour = colourdict[section][0]

        # fig.add_trace(go.Scattergeo(
        #             lon=[i[0] for i in positions],
        #             lat=[i[1] for i in positions],
        #             mode="markers",
        #             text=np.arange(0,400,1),
        #             marker=dict(color=colour, size=10))
        # )
        for i in range(len(shortest_path)-1):
            source = shortest_path[i]
            destination = shortest_path[i+1]
            fig.add_trace(go.Scattermapbox(
                lon=[positions[source][0], positions[destination][0]],
                lat=[positions[source][1], positions[destination][1]],
                mode="lines",
                line=dict(width=2, color=colourdict[section][0]) 
                ))
        
        if all_edges:
            for i in range(len(all_edges)-1):
                source, destination = all_edges[i]
                # destination = shortest_path[i+1]
                fig.add_trace(go.Scattermapbox(
                    lon=[positions[source][0], positions[destination][0]],
                    lat=[positions[source][1], positions[destination][1]],
                    mode="lines",
                    line=dict(width=1, color='blue') 
                    ))

    return fig

def plotCircle(R, centre, fig):
    thetas = np.linspace(0,2*math.pi, 100)
    # centre = [-74,40.7]
    R = R/111E3
    xs = [centre[0] + R*math.cos(theta) for theta in thetas]
    ys = [centre[1] + R*math.sin(theta) for theta in thetas]

    fig.add_trace(go.Scattermapbox(
                lon=xs,
                lat=ys,
                mode="lines",
                line=dict(width=2, color='green') 
                ))
    return fig
            # bearing=0,
            # center=dict(
            #     lat=45.8257,
            #     lon=10.8746, 
            # ),
            # pitch=0,
            # zoom=5.6,
            # style='outdoors')
    # )
    # fig.show()

# print(calcDistanceBetween(0,10))
# plot()