import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import pickle as pck
import numpy as np
import matplotlib.pyplot as plt
from dijkstra import calcDistanceBetween, plotPath, plotCircle
from geometry import find_sat, fetch_locs, fetch_curr, Phases, colourdict, Locations, fetch_cart, findrange
import time as tm
from copy import deepcopy

# try:
#     print('Reading graphdict file....')
#     graphdict = pck.load(open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'rb'))
#     print('File opened.')
# except:
#     pck.dump([], open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'wb'))


def createNetworkGraph(time):
    section = 1
    longitudes, latitudes = fetch_locs(section, time)
    positions = fetch_cart(section, time)
    G=nx.Graph()
    geopositions = list(zip(longitudes, latitudes))
    edges = 0
    all_edges = []
    for source_sat in range(len(positions)):
        source_loc = positions[source_sat]
        for neighbour_sat in range(len(positions)):
            neighbour_loc = positions[neighbour_sat]
            distance = np.round(calcDistanceBetween(source_loc, neighbour_loc),0)
            # print(source_loc, neighbour_loc)
            # print(distance, Phases['max comms range'][section-1])
            # if (source_loc[0] == -15.57) and (neighbour_loc[0] == -21.66):
            # print(source_sat, neighbour_sat, distance, Phases['max comms range'][section-1])
            if distance < Phases['max comms range'][section-1]:
                # print(distance, Phases['max comms range'][section-1])
                if source_sat == 724 and neighbour_sat == 769:
                    print(distance)
                edges+=1
                all_edges.append([source_sat, neighbour_sat])
                G.add_edge(source_sat,neighbour_sat, weight=distance)
    print('edges:', edges)
    return G, geopositions#, all_edges

def calcPath(source, destination, time, graphdict):
    # G, positions = graphdict[str(time)]
    # [G, positions] = pck.load(open('data/'+str(int(Phases['Altitude'][section-1]/1E3))+'/'+str(time)+'.pck', 'rb'))
    [G, positions] = graphdict[str(time)]

    source_sat, source2ground = find_sat(source, positions)
    dest_sat, dest2ground = find_sat(destination, positions)        
    tic = tm.time()
    shortest_path = nx.single_source_dijkstra(G, source_sat, dest_sat,weight='weight')
    shortest_path[0] = shortest_path[0] + source2ground + dest2ground
    print(tm.time()- tic)
    return shortest_path, positions

def onePlot(loc1, loc2, graphdict):
    mapbox_access_token = open(".mapbox_token").read()

    # graphdict = pck.load(open('data/graphdict'+str(int(Phases['Altitude'][0]/1E3))+'.pck', 'rb'))
    fig = go.Figure(
                data=[go.Scattermapbox(lon=[], lat=[],
                    name="frame",
                    mode="markers",
                    marker=go.scattermapbox.Marker(size=5, color='red'))],
                layout=go.Layout(
                    xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
                    yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
                    height = 1000,
                    width = 1500,
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
        fig.add_trace(go.Scattermapbox(lon=longitudes, lat=latitudes,
                        name="frame",
                        mode="markers",
                        marker=go.scattermapbox.Marker(size=7, color='red')))

        # for live dijkstra plotting when all positions have been calculated
        source = Locations[loc1]
        destination = Locations[loc2]
        # fig = plotCircle(Phases['max ground reach'][i], source, fig)
        # fig = plotCircle(Phases['max ground reach'][i], destination, fig)

        [G, positions] = graphdict[str(time)]
        # findrange(source, positions, fig)
        # findrange(destination, positions, fig)
        fig.add_trace(go.Scattermapbox(lon=[source[0], destination[0]], lat=[source[1], destination[1]],
                        name="frame",
                        mode="markers",
                        marker=go.scattermapbox.Marker(size=10, color='green')))
        shortest_path, positions = calcPath(source, destination, int(np.floor(time/10)*10), graphdict)
        # shortest_path = calcPath(source, destination, time, graphdict)

        fig.add_annotation(
            text="Time Elapsed: "+str(time)+"s, Shortest Path Latency: "+str(np.round(shortest_path[0]/300E3,3))+"ms",#, Path: "+str([str(i) for i in shortest_path[1]]),
            showarrow=False,
            yshift=-270, font=dict(size=18))
        fig.add_annotation(
            text="Path: "+str([str(i) for i in shortest_path[1]])+', Hop count: '+str(len(shortest_path[1])),
            showarrow=False,
            yshift=-300, font=dict(size=18))
        fig = plotPath(shortest_path[1], positions, fig)
        fig.update_layout(showlegend=False,  
        mapbox=dict(
            accesstoken=mapbox_access_token, 
            style='light',
            zoom=1.4))
        fig.show()

# G, positions = createNetworkGraph(10)
# source = Locations['New York']
# destination = Locations['Singapore']
# source_sat = find_sat(source, positions)
# dest_sat = find_sat(destination, positions)
# shortest_path = nx.single_source_dijkstra(G, source_sat, dest_sat,weight='weight')
# print(shortest_path)
# fig = plotPath(shortest_path[1], positions)
# fig.show()

# graphdict = {}
# section=1
# print('reading dicts')
# for i in np.arange(10,1000, 10):
#     graphdict[str(i)] = pck.load(open('data/'+str(int(Phases['Altitude'][section-1]/1E3))+'/'+str(i)+'.pck', 'rb'))
# print('dicts read')

# onePlot('London', 'Singapore', graphdict)
# Draw networkx network:
# [G, positions] = pck.load(open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'/'+str(10)+'.pck', 'rb'))

# pos = nx.spiral_layout(G)
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
# nx.draw_networkx_edges(G,pos)
# nx.draw(G)
# plt.show()