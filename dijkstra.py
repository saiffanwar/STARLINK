import numpy as np
from geometry import *
from pprint import pprint
from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle as pck


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
    distance = np.sqrt((((source_loc[0] - dest_loc[0])*111.32E3)**2)+(((source_loc[1] - dest_loc[1])*111E3)**2))
    return distance


def drawEdges(section, sat1, planedfs, fig):
    planeNumber, satNumber = sat1
    satAttributes = planedfs[str(section)].iloc[planeNumber][satNumber]
    print(planedfs[str(section)].iloc[planeNumber][satNumber]['Neighbours'])
    
    
    # for [neighbourPlane, neighbourSat] in satAttributes['Neighbours'][0]:
    #     print(type(neighbourPlane), type(neighbourSat))
    #     fig.add_trace(go.Scatter(
    #             x=[planedfs[str(section)].iloc[planeNumber][satNumber]['Realigned Longitude'], 
    #                 planedfs[str(section)].iloc[neighbourPlane][neighbourSat]['Realigned Longitude']],
    #             y=[planedfs[str(section)].iloc[planeNumber][satNumber]['Latitude'], 
    #                 planedfs[str(section)].iloc[neighbourPlane][neighbourSat]['Latitude']],
    #             mode="lines",
    #             line=dict(width=2, color=colourdict[section][0], 
    #             )
    # ))

def createDF(t):
    planedfs = {}
    # source_sat = [90.75,36.74]
    for section in range(1,2):
        longitudes, latitudes = fetch_locs(section,t)
        no_of_planes = Phases['Planes'][section-1]
        sats_per_plane = Phases['Sats per plane'][section-1]
        colour = colourdict[section][0]
        longitudes = list(chunks(longitudes, sats_per_plane))
        latitudes = list(chunks(latitudes, sats_per_plane))
        planedfs[str(section)] = pd.DataFrame(index=np.arange(no_of_planes), columns=np.arange(sats_per_plane))

        for i in range(no_of_planes):
            planedfs[str(section)].iloc[i] = [{'Longitude': longitudes[i][j],
                                                # 'Realigned Longitude': realignment(longitudes[i][j], source_sat), 
                                                'Latitude': latitudes[i][j]} for j in range(sats_per_plane)]
                                                # 'Neighbours': find_neighbours(i,j, longitudes)} for j in range(sats_per_plane)]
    return planedfs

def plot(shortest_path, planedfs, fig=None):
    if not fig:
        fig = go.Figure(go.Scatter( 
                        x=[],y=[],
                        ))
    for section in range(1,2):
        no_of_planes = Phases['Planes'][section-1]
        sats_per_plane = Phases['Sats per plane'][section-1]
        colour = colourdict[section][0]
        shortest_path = [divmod(i, sats_per_plane) for i in shortest_path[1]]
        # fig = go.Figure(go.Scatter( 
        #                 x=[],y=[],
        #                 ))
        # fig.add_trace(go.Scatter(
        #                     x=[planedfs[str(section)].iloc[i][j]['Longitude'] for i in range(no_of_planes) for j in range(sats_per_plane)],
        #                     y=[planedfs[str(section)].iloc[i][j]['Latitude'] for i in range(no_of_planes) for j in range(sats_per_plane)],
        #                     mode="markers",
        #                     marker=dict(color=colour, size=5))
        # )
        fig.add_trace(go.Scatter(
                    x=[planedfs[str(section)].iloc[i][j]['Longitude'] for i in range(no_of_planes) for j in range(sats_per_plane)],
                    y=[planedfs[str(section)].iloc[i][j]['Latitude'] for i in range(no_of_planes) for j in range(sats_per_plane)],
                    mode="markers",
                    marker=dict(color=colour, size=8))
        )
        for i in range(len(shortest_path)-1):
            fig.add_trace(go.Scatter(
                x=[planedfs[str(section)].iloc[shortest_path[i][0]][shortest_path[i][1]]['Longitude'], 
                    planedfs[str(section)].iloc[shortest_path[i+1][0]][shortest_path[i+1][1]]['Longitude']],
                y=[planedfs[str(section)].iloc[shortest_path[i][0]][shortest_path[i][1]]['Latitude'], 
                    planedfs[str(section)].iloc[shortest_path[i+1][0]][shortest_path[i+1][1]]['Latitude']],
                mode="lines",
                line=dict(width=2, color=colourdict[section][0]) 
                ))
    return fig
    # fig.show()


# plot()