import numpy as np
from geometry import *
from pprint import pprint
from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx

def chunks(lst,n):
    for i in range(0, len(lst), n):
            yield lst[i:i + n]


def find_edges(satPlaneNumber, satNumber, longitudes):

    sats_per_plane = len(longitudes[0])
    no_of_planes = len(longitudes)
    edges = []
    if satNumber == 0:
        edges.append([satPlaneNumber, sats_per_plane])
        edges.append([satPlaneNumber, satNumber + 1])
    elif satNumber == sats_per_plane:
        edges.append([satPlaneNumber, 0])
        edges.append([satPlaneNumber, satNumber - 1])
    else:
        edges.append([satPlaneNumber, satNumber - 1])
        edges.append([satPlaneNumber, satNumber + 1])

    if satPlaneNumber == 0:
        edges.append([no_of_planes,satNumber])
        edges.append([satPlaneNumber + 1,satNumber])
    elif satPlaneNumber == no_of_planes:
        edges.append([0,satNumber])
        edges.append([satPlaneNumber - 1,satNumber])
    else:
        edges.append([satPlaneNumber - 1, satNumber])
        edges.append([satPlaneNumber + 1, satNumber])
    return edges

# Realigns the ground map of satellites so that the starting satellite is in the centre.
# This means the furthest we can possibly travel is at the edge of the 2d map and removes need for cycling later on.
# This also halves the time complexity because we know which side of the map the destination is located
def realignment(longitudes, central_sat):
    # sat_numbers = np.arange(0,len(longitudes),1)
    new_lons = []
    if central_sat[0] >= 0:
        for og_lon in longitudes:
            if og_lon < (-180 + central_sat[0]):
                new_lon = -360 - og_lon + central_sat[0]
            else:
                new_lon = -(og_lon - central_sat[0])
            new_lons.append(new_lon)
    elif central_sat[0] < 0:
        for og_lon in longitudes:
            if og_lon > (180 + central_sat[0]):
                new_lon = 360 - og_lon + central_sat[0]
            else:
                new_lon = -(og_lon - central_sat[0])
            new_lons.append(new_lon)
    return new_lons

# Returns the distance between 2 satellites in km.
# Distance between deg of longitude is 111.32km.
# Distance between deg of latitude is 111km.
def calc_distanceBetween(sat1, sat2, longitudes, latitudes):
    sat1_loc = [longitudes[sat1], latitudes[sat1]]
    sat2_loc = [longitudes[sat2], latitudes[sat2]]
    distance = np.sqrt((((sat1_loc[0] - sat2_loc[0])*111.32)**2)+(((sat1_loc[1] - sat2_loc[1])*111)**2))
    return sat1_loc, sat2_loc



fig = go.Figure(go.Scatter( 
                x=[],y=[],
                # x=realigned_sats['Realigned Longitude'],
                # x=realigned_sats['Old Longitude'],
                # y=realigned_sats['Latitude'],
                ))


planedfs = {}
for deployment in range(1,3):
    longitudes, latitudes, no_of_planes, sats_per_plane, colour = fetch_locs(deployment)
    longitudes = list(chunks(longitudes, sats_per_plane))
    latitudes = list(chunks(latitudes, sats_per_plane))
    planedfs[str(deployment)] = pd.DataFrame(index=np.arange(len(longitudes)), columns=np.arange(len(longitudes[0])))

    for i in range(len(longitudes)):
        planedfs[str(deployment)].iloc[i] = [[longitudes[i][j], latitudes[i][j],find_edges(i,j, longitudes)] for j in range(len(longitudes[i]))]

    fig.add_trace(go.Scatter(
                x=realigned_sats['Old Longitude'],
                y=realigned_sats['Latitude'],
                mode="markers",
                marker=dict(color=colour, size=5))
    )
   
    realigned_lons = realignment(np.array(longitudes).flatten(), [len(longitudes[0]),0])
    realigned_sats = pd.DataFrame({
        'Old Longitude': np.array(longitudes).flatten(),
        'Realigned Longitude': realigned_lons,
        'Latitude': np.array(latitudes).flatten(),
    })

    # fig.add_trace(go.Scatter(
    #             x=realigned_sats['Realigned Longitude'],
    #             y=realigned_sats['Latitude'],
    #             mode="markers",
    #             marker=dict(color=colour, size=5),
    #             text=np.arange(0,len(longitudes),1)
    # ))


# def shortest_path():

# for i,j in zip(longitudes, latitudes):
# #     sat1, sat2 = calc_distanceBetween(i, j, realigned_lons, latitudes)


fig.show()



