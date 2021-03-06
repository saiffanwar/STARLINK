import networkx as nx
import string
from sim_utils import calcDistanceBetween, Phases
import numpy as np



def double_graph(m,n, positions):
    
    G=nx.Graph()
    letters = string.ascii_letters

    level = letters[0:m]
    for l in level:
        for i in range(1, n + 1):
            G.add_node(l+str(i))
            
    for u in G.nodes:
        
        prev_level = letters[letters.index(u[0]) - 1]
        next_level = letters[letters.index(u[0]) + 1]
        
        indu = int(''.join(i for i in u if i.isdigit()))
    
        for v in G.nodes:
            indv = int(''.join(i for i in v if i.isdigit()))
            
            if u.startswith(v[0]) and indu == indv - 1:
                G.add_edge(u, v)
            
            if v[0] == next_level and indu == indv - 1:
                G.add_edge(u, v)
                
            if v[0] == prev_level and indu == indv - 1:
                G.add_edge(u, v)    
                
            if indv == n and indu == 1 and (v[0] in [prev_level, u[0], next_level]):
                G.add_edge(u, v)
                
    pos = 0
    nodes = {}
    for l in level:
        for i in range(1, n + 1):
            nodes[l+str(i)] = positions[pos]
            pos+=1
    for i in G.edges:
        distance = np.round(calcDistanceBetween([nodes[i[0]][0], nodes[i[0]][1], nodes[i[0]][2]], [nodes[i[1]][0], nodes[i[1]][1], nodes[i[1]][2]]),0)
        if distance > Phases['max comms range'][1-1]:
            G.remove_edge(i[0], i[1])

    return G, nodes



#---------------- Compute shortest paths
# matrix_distance = {}

# for e in G.edges:
#     matrix_distance[e] = np.random.uniform(5,45,1)[0] # random distance (5km - 45km)
    
# nx.set_edge_attributes(G, matrix_distance, name = 'weight')

# max_distance = None # maximum distance allowed (km)

# S = dict(nx.all_pairs_dijkstra_path(G, max_distance, 'weight')) # return all shortest paths
# D = dict(nx.all_pairs_dijkstra_path_length(G, max_distance, 'weight')) # return all shortest paths length (km)

# S['a1']['j1'] # shortest path between a1 and j1
# D['a1']['j1'] # distance between a1 and j1 (km)

# #--- Shortest paths by number of hops

# S = dict(nx.all_pairs_dijkstra_path(G, max_distance, None))
# D = dict(nx.all_pairs_dijkstra_path_length(G, max_distance, None)) # return all shortest paths length (hops)

# S['a1']['j1'] 
# D['a1']['j1'] # distance between a1 and j1 (hops)