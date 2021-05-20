from sim_ops import phase
import numpy as np
from dijkstra import calcDistanceBetween
import pickle as pck
from geometry import Phases

min_distances = []
for offsets in np.arange(1,72,2):
    sats, starting_positions = phase(1,offsets)
    curr_min = None
    for i in starting_positions:
        for j in starting_positions:
            if i != j:
                distance = calcDistanceBetween(i,j)
                # curr_min = distance
                if not curr_min:
                    curr_min = distance
                elif distance < curr_min:
                    curr_min = distance
    min_distances.append(curr_min)
    print(distance)
    print(curr_min)
    print(min_distances)
    with open('data/'+str(int(Phases['Altitude'][1-1]/1E3))+'/offsets.pck', 'wb') as f:
            pck.dump(min_distances, f)
