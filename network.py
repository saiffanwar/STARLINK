import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import pickle as pck
import numpy as np
import matplotlib.pyplot as plt
from path_utils import plotPathgeo
from sim_utils import find_sat, fetch_locs, fetch_curr, fetch_cart, calcDistanceBetween, Phases, colourdict, Locations, findrange
import time as tm
from copy import deepcopy


# def createNetworkGraph(phasenum, time):
#     longitudes, latitudes = fetch_locs(phasenum, time)
#     positions = fetch_cart(phasenum, time)
#     G=nx.Graph()
#     geopositions = list(zip(longitudes, latitudes))
#     for source_sat in range(len(positions)):
#         source_loc = positions[source_sat]
#         for neighbour_sat in range(len(positions)):
#             neighbour_loc = positions[neighbour_sat]
#             distance = np.round(calcDistanceBetween(source_loc, neighbour_loc),0)

#             if distance < Phases['max comms range'][phasenum-1]:
#                 G.add_edge(source_sat,neighbour_sat, weight=distance)
#     return G, geopositions

def createNetworkGraph(phasenum, time):
    longitudes, latitudes = fetch_locs(phasenum, time)
    positions = fetch_cart(phasenum, time)
    G=nx.Graph()
    geopositions = list(zip(longitudes, latitudes))
    for source_sat in range(len(positions)):
        satnum = divmod(source_sat, Phases['Sats per plane'][phasenum-1])
        if satnum[1] != 0 and Phases['Sats per plane'][phasenum-1]:
            satbefore = satnum[1] - 1
            satafter = satnum[1] +1
        elif satnum[1] == 0:
            satafter = 1
            satbefore = Phases['Sats per plane'][phasenum-1]
        elif satnum[1] == Phases['Sats per plane'[phasenum-1]]:
            satafter = 0
            satbefore = Phases['Sats per plane'][phasenum-1] -1
        neighbours = [satnum[0]*Phases['Sats per plane'][phasenum-1] + satafter, satnum[0]*Phases['Sats per plane'][phasenum-1] + satbefore]
        print(neighbours)
        # for neighbour_sat in range(len(positions)):
        #     neighbour_loc = positions[neighbour_sat]
        #     distance = np.round(calcDistanceBetween(source_loc, neighbour_loc),0)

            # if distance < Phases['max comms range'][phasenum-1]:
        G.add_edge(source_sat,satnum[0]*Phases['Sats per plane'][phasenum-1] + satafter, weight=0)
        G.add_edge(source_sat,satnum[0]*Phases['Sats per plane'][phasenum-1] + satbefore, weight=0)
    return G, geopositions

def calcPath(phasenum, source, destination, time, graphdict=None):

    [G, positions] = pck.load(open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/'+str(time)+'.pck', 'rb'))

    tic = tm.time()
    source_sat, source2ground = find_sat(phasenum, source, positions)
    source_calc_time1 = tm.time() - tic
    tic = tm.time()
    dest_sat, dest2ground = find_sat(phasenum, destination, positions)        
    dest_calc_time1 = tm.time() - tic


    shortest_path = list(nx.single_source_dijkstra(G, source_sat, dest_sat,weight='weight'))
    path = shortest_path[1]
    rtt = shortest_path[0] + source2ground + dest2ground

    return rtt, path, positions


# This function is used to create a static path image.
def onePlot(loc1, loc2, time):
    mapbox_access_token = open(".mapbox_token").read()
    fig = go.Figure(
                data=[go.Scattermapbox(lon=[], lat=[],
                    name="frame",
                    mode="markers",
                    marker=go.scattermapbox.Marker(size=5, color='red'))],
                layout=go.Layout(
                    xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
                    yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
                    height = 500,
                    width = 800
                    ))

    for phasenum in range(1,2):
        longitudes, latitudes = fetch_locs(phasenum, time)
        fig.add_trace(go.Scattermapbox(lon=longitudes, lat=latitudes,
                        name="frame",
                        mode="markers",
                        text = np.arange(0,Phases['Planes'][phasenum-1]*Phases['Sats per plane'][phasenum-1],1),
                        marker=go.scattermapbox.Marker(size=5, color=colourdict[phasenum][0])))

        source = Locations[loc1]
        destination = Locations[loc2]


        fig.add_trace(go.Scattermapbox(lon=[source[0], destination[0]], lat=[source[1], destination[1]],
                        name="frame",
                        mode="markers",
                        marker=go.scattermapbox.Marker(size=10, color='green')))
        rtt, path, positions = calcPath(phasenum, source, destination, time)

        fig.add_annotation(
            text="Time Elapsed: "+str(time)+"s, Round Trip Time: "+str(2*np.round(rtt/300E3,3))+"ms",
            showarrow=False,
            yshift=-185, font=dict(size=18))
        fig.add_annotation(
            text="Path: "+str([str(i) for i in path])+', Hop count: '+str(2*(len(path)+2)),
            showarrow=False,
            yshift=-205, font=dict(size=18))
        fig = plotPathgeo(source, destination, phasenum, path, positions, fig)
        fig.update_layout(showlegend=False,  
        mapbox=dict(
            accesstoken=mapbox_access_token, 
            style='light', zoom=0.7))
    # fig.write_image('figs/exp2/'+str(loc1)+str(loc2)+'longest.pdf')
    fig.show()



# The code below can be used to observe the Network graph at a specific timepoint. They are humanly incomprehensible.
# [G, positions] = createNetworkGraph(1,0)
# # [G, positions] = pck.load(open('data/'+str(int(Phases['Altitude'][1-1]/1E3))+'/'+str(0)+'.pck', 'rb'))

# pos = nx.circular_layout(G)
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
# nx.draw_networkx_edges(G,pos)
# nx.draw(G)
# plt.show()