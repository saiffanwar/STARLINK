from sim_utils import calcDistanceBetween, fetch_curr, fetch_cart, Phases
import numpy as np 
import pandas as pd 
from pprint import pprint
# longitudes, latitudes = fetch_curr(1)
positions = fetch_cart(1, 0)
tot_distances = []
<<<<<<< HEAD


=======
print(len(positions))
print(Phases['max comms range'][1-1])
>>>>>>> 10270f399f2c100c8eed545117032bd878b425ac
for source_sat in range(len(positions)):
    source_loc = positions[source_sat]
    curr_distances = []
    for neighbour_sat in range(len(positions)):
        neighbour_loc = positions[neighbour_sat]
        distance = np.round(calcDistanceBetween(source_loc, neighbour_loc),0)
        if distance < Phases['max comms range'][1-1]:
            curr_distances.append(distance)
        else:
            curr_distances.append(None)
    tot_distances.append(curr_distances)

df = pd.DataFrame(tot_distances)
df.to_csv('40sats.csv')

pprint(df)





