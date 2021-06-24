from sim_ops import phase, orbit
import os
import threading
import click
import pickle as pck 
from pprint import pprint
import argparse

parser = argparse.ArgumentParser(description='Simulation setup')

parser.add_argument('--phasenums', default=1,
                    help='number of phases to deploy in the simulation')
<<<<<<< HEAD
parser.add_argument('--time_limit', default=100,
=======
parser.add_argument('--time_limit', default=1,
                    help='number of phases to deploy in the simulation')
parser.add_argument('--pathfinder', default='ON',
>>>>>>> 10270f399f2c100c8eed545117032bd878b425ac
                    help='number of phases to deploy in the simulation')
parser.add_argument('--pathfinder', default='OFF',
                    help='Find the shortest paths of the routes specified')
parser.add_argument('--getGraphs', default='OFF',
                    help='Whether to compute network graphs')
args = parser.parse_args()

#All LEO satellites
phase_sats = []
# phasenums=3
for phasenum in range(1,int(args.phasenums)+1):        
    phase_sats.append(phase(phasenum))

for i in phase_sats:
    if args.getGraphs == 'ON':
        threading.Thread(target=orbit, args=(i, 1, int(args.time_limit), True)).start()
 
    else:
        threading.Thread(target=orbit, args=(i, 1, int(args.time_limit))).start()



if args.pathfinder == 'ON':
    os.system('python app.py')