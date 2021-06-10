from network import createNetworkGraph
import pickle as pck
# from geometry import Phases
from sim_utils import Phases
from pprint import pprint
import multiprocessing as mp
from tqdm import tqdm
import threading
import numpy as np
import time as tm
import argparse
import os


def graphFromPos(phasenum, times, chunk):

    graphdict = {}
    with open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+str(chunk)+'.pck', 'wb') as f:
        pck.dump(graphdict, f)
    print(times, chunk)
    for i in times:
        if i != 0:
            if i%1 ==0:
                tic = tm.time()
                G, positions = createNetworkGraph(phasenum, i)
                graphdict[str(i)] = [G, positions]
                print(i,': ', tm.time()-tic)
                print(graphdict.keys())
                print('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/'+str(i)+'.pck')
                with open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/'+str(i)+'.pck', 'wb') as f:
                    pck.dump(graphdict[str(i)], f)
    print('saved')
        
def chunks(lst,workers=4):
    print(len(lst))
    n = int(len(lst)/workers)
    for i in range(0, len(lst), n):
            yield lst[i:i + n]


def compute_graphs(time_limit, phasenum=1):
    times = np.arange(0,time_limit,1)
    times = chunks(times)
    if __name__ == '__main__':
        jobs = []
        for i, chunk in zip(times,[0,1,2,3]):
            p = mp.Process(target=graphFromPos, args=(phasenum, i,chunk,))
            jobs.append(p)
            p.start()

# os.system('python3 startsim.py  --pathfinder OFF --time_limit '+str(args.time))
compute_graphs(int(input('How many seconds would you like to compute graphs for?')))