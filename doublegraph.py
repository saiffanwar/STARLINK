import networkx as nx
import matplotlib.pyplot as plt
import string

G = nx.Graph()

n = 10
m = 10

letters = string.ascii_letters

level = letters[0:m]
no_of_sats=20
# for i in range(no_of_sats):
#         G.add_node(i)

# print(G.nodes)


for l in level:
    for i in range(1, n + 1):
        G.add_node(l+str(i))

print(G.nodes)

for u in G.nodes:
    # print(u)
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

nx.draw(G, with_labels = True)
