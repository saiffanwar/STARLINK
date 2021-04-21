import networkx as nx
import pandas as pd
import pickle as pck
import numpy as np
import matplotlib.pyplot as plt
from dijkstra import * 
import time

def createNetworkGraph(graphdict, time):
    # tic  = time.time()
    planedfs = createDF()
    # print(time.time() - tic)
    for section in range(1,2):
        no_of_planes = Phases['Planes'][section-1]
        sats_per_plane = Phases['Sats per plane'][section-1]
        altitude = Phases['Altitude'][section-1]

        max_comms_range = np.sqrt(((earth_radius+altitude)**2) - (earth_radius**2)) 
        dest_sat = []

        G=nx.Graph()
        for i in range(no_of_planes):
            for j in range(sats_per_plane):
                source_loc = [planedfs[str(section)].iloc[i][j]['Longitude'],
                                planedfs[str(section)].iloc[i][j]['Latitude']]
                # for k,l in planedfs[str(section)].iloc[i][j]['Neighbours'][0]:
                for k in range(no_of_planes):
                    for l in range(sats_per_plane):
                        neighbour_loc = [planedfs[str(section)].iloc[k][l]['Longitude'],
                                    planedfs[str(section)].iloc[k][l]['Latitude']]
                        distance = np.round(calcDistanceBetween(source_loc,neighbour_loc),0)
                        # print(planedfs[str(section)].iloc[i][j]['Longitude'],planedfs[str(section)].iloc[k][l]['Longitude'])
                        if distance < max_comms_range:
                            G.add_edge((i*sats_per_plane)+j,(k*sats_per_plane)+l, weight=distance)

    # with open('network_df.pck', 'wb') as f:
    #     pck.dump([G,planedfs], f)
    graphdict[str(time)] = [G,planedfs]
    return graphdict


# graphdict = createNetworkGraph({},0)
# with open('graphdict.pck', 'rb') as f:
#         graphdict = pck.load(f)
# print(graphdict)

# networkdf = graphdict['0']
# G = networkdf[0]
# planedfs = networkdf[1]
# shortest_path = nx.single_source_dijkstra(G, 23,43,weight='weight')
# print('Shortest Path Latency: ', shortest_path[0]/300E6)
# fig = plot(shortest_path, planedfs)
# fig.show()
# pos = nx.spiral_layout(G)
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
# nx.draw_networkx_edges(G,pos)
# nx.draw(G)
# plt.show()