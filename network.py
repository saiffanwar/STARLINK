import networkx as nx
import pandas as pd
import pickle as pck
import numpy as np
import matplotlib.pyplot as plt
from dijkstra import * 
from geometry import find_sat
import time
from copy import deepcopy

def createNetworkGraph(time):
    section = 1
    longitudes, latitudes = fetch_locs(section, time)
    G=nx.Graph()
    positions = list(zip(longitudes, latitudes))
    edges = 0
    all_edges = []
    for source_sat in range(len(longitudes)):
        source_loc = positions[source_sat]
        for neighbour_sat in range(len(longitudes)):
            neighbour_loc = positions[neighbour_sat]
            distance = np.round(calcDistanceBetween(source_loc, neighbour_loc),0)
            # if (source_loc[0] == -15.57) and (neighbour_loc[0] == -21.66):
            # print(source_sat, neighbour_sat, distance, Phases['max comms range'][section-1])
            if distance < Phases['max comms range'][section-1]:
                # print(distance, Phases['max comms range'][section-1])
                edges+=1
                all_edges.append([source_sat, neighbour_sat])
                G.add_edge(source_sat,neighbour_sat, weight=distance)
    print('edges:', edges)
    return G, positions#, all_edges


# graphdict = pck.load(open('data/graphdict'+str(int(Phases['Altitude'][0]/1E3))+'.pck', 'rb'))

def calcPath(source, destination, time, graphdict):
    G, positions = graphdict[str(time)]
    source_sat = find_sat(source, positions)
    dest_sat = find_sat(destination, positions)
    shortest_path = nx.single_source_dijkstra(G, source_sat, dest_sat,weight='weight')

    return shortest_path, positions

# Draw networkx network:
# pos = nx.spiral_layout(G)
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
# nx.draw_networkx_edges(G,pos)
# nx.draw(G)
# plt.show()