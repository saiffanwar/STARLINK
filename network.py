import networkx as nx
import pandas as pd
import pickle as pck
import numpy as np
import matplotlib.pyplot as plt
from dijkstra import * 
from geometry import *
import time
from copy import deepcopy
# def createNetworkGraph(graphdict, time):
#     # tic  = time.time()
#     planedfs = createDF(time)
#     # print(time.time() - tic)
#     for section in range(1,2):
#         no_of_planes = Phases['Planes'][section-1]
#         sats_per_plane = Phases['Sats per plane'][section-1]
#         altitude = Phases['Altitude'][section-1]

#         max_comms_range = np.sqrt(((earth_radius+altitude)**2) - (earth_radius**2)) 
#         dest_sat = []

#         G=nx.Graph()
#         for i in range(no_of_planes):
#             for j in range(sats_per_plane):
#                 source_loc = [planedfs[str(section)].iloc[i][j]['Longitude'],
#                                 planedfs[str(section)].iloc[i][j]['Latitude']]
#                 # for k,l in planedfs[str(section)].iloc[i][j]['Neighbours'][0]:
#                 for k in range(no_of_planes):
#                     for l in range(sats_per_plane):
#                         neighbour_loc = [planedfs[str(section)].iloc[k][l]['Longitude'],
#                                     planedfs[str(section)].iloc[k][l]['Latitude']]
#                         distance = np.round(calcDistanceBetween(source_loc,neighbour_loc),0)
#                         # print(planedfs[str(section)].iloc[i][j]['Longitude'],planedfs[str(section)].iloc[k][l]['Longitude'])
#                         if distance < max_comms_range:
#                             G.add_edge((i*sats_per_plane)+j,(k*sats_per_plane)+l, weight=distance)

#     # with open('network_df.pck', 'wb') as f:
#     #     pck.dump([G,planedfs], f)
#     graphdict[str(time)] = [G,planedfs]
#     return graphdict



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
    # graphdict[str(time)] = [G,positions]
    # with open('graphdict.pck', 'wb') as f:
    #         pck.dump(graphdict, f)
    # print(graphdict)
    print('edges:', edges)
    return G, positions#, all_edges


section=1
graphdict = pck.load(open('data/graphdict'+str(int(Phases['Altitude'][section-1]/1E3))+'.pck', 'rb'))

# print(graphdict.items())
# tic = time.time()
# # graphdict = createNetworkGraph({},10)
# print(time.time() -tic)
G, positions = graphdict['10']
source_sat = find_sat(Locations['London'], positions)
dest_sat = find_sat(Locations['Johannesburg'], positions)

shortest_path = nx.single_source_dijkstra(G, source_sat, dest_sat,weight='weight')


print(shortest_path)
print('Shortest Path Latency: ', shortest_path[0]/300E6)
fig = plot(shortest_path[1], positions)
fig.show()

# pos = nx.spiral_layout(G)
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
# nx.draw_networkx_edges(G,pos)
# nx.draw(G)
# plt.show()
