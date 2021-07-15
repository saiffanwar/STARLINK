import networkx as nx
import string

def double_graph(m,n):
    
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

    return G