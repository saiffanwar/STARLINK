from geometry import Locations, Phases, fetch_curr, calcDistanceBetween
from network import calcPath
import pickle as pck
import numpy as np
from matplotlib import pyplot as plt
# from sim_ops import phase
# source = Locations['New York']
# destination = Locations['London']
# try:
#     print('Reading graphdict file....')
#     graphdict = pck.load(open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'rb'))
#     print('File opened.')
# except:
#     pck.dump([], open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'wb'))
# ys = []
# for i in np.arange(10,1000,10):
#     shortest_path, positions = calcPath(source, destination, i, graphdict)
#     ys.append(np.round(2*shortest_path[0]/300E3,3))

# plt.plot(np.arange(10,1000,10), ys)
# plt.show()

# min_distances = []
phase_offsets = np.arange(0,72,1)
# for i in phase_offsets:
#     phase_sats1 = phase(1, i)
#     longitudes, latitudes, positions = fetch_curr(1)
#     min_distance=None
#     for i in list(zip(longitudes, latitudes)):
#         for j in list(zip(longitudes, latitudes)):
#             if i != j:
#                 distance= calcDistanceBetween(i,j)
#                 if not min_distance:
#                     min_distance= calcDistanceBetween(i,j)
#                 elif distance < min_distance:
#                     min_distance= distance
#     print(min_distance)
#     min_distances.append(min_distance)
# print(phase_offsets)
# print(min_distances)
min_distances = [5979.912788661537, 22122.382616707047, 42552.37948693344, 4975.522871014899, 28040.008756062394, 17937.123265451515, 4975.522871014899, 12210.0, 41719.0040628969, 5550.0, 23183.004823361065, 5550.0, 6770.805907718671, 17977.174527717674, 41719.0040628969, 3519.2368718231332, 18974.43840117588, 7860.207121951613, 1113.1999999989876, 12996.596779156924, 16978.85763412786, 1113.2000000005696, 18974.438401175743, 11619.394304351063, 6679.200000000254, 20668.029007140434, 17235.136432299772, 3519.2368718233834, 23919.651154647698, 13917.464303528925, 10080.10185662861, 18655.86624737609, 14044.565776127953, 1109.9999999997792, 7038.473743646767, 9487.21920058775, 4010.153134233235, 26848.510725178054, 15930.562029005401, 4010.153134233235, 15720.414243905021, 11004.289970734746, 3519.236871823321, 35111.41444032105, 24515.541849202382, 2483.468187837182, 11984.783018479196, 9566.81753562723, 5992.391509240187, 40320.40742651287, 16527.39916139381, 12678.692891619708, 5555.76530821685, 18356.26447401501, 4975.52287101627, 29990.66711895555, 11984.783018477434, 9951.045742031301, 10493.43658483554, 3519.236871823071, 3511.141444031831, 23238.788608705232, 12260.640857638855, 3511.141444031831, 11351.203636618628, 17845.754269293695, 7038.4737436462665, 9178.132237009137, 14640.888175246693, 14044.565776129704, 15720.414243905581, 15499.345359078947]

plt.bar(phase_offsets[1::2], [i/1000 for i in min_distances[1::2]])
plt.show()