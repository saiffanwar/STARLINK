from sat_ops import Phase
import argparse
import threading
import vpython as vp
import math
import numpy as np
from sim_utils import Phases, colourdict, speed, calcGCR

parser = argparse.ArgumentParser(description='Simulation setup')

parser.add_argument('--phasenums', default=1,
                    help='number of phases to deploy in the simulation')
parser.add_argument('--time_limit', default=10000000,
                    help='number of phases to deploy in the simulation')
parser.add_argument('--pathfinder', default='ON',
                    help='Find the shortest paths of the routes specified')
parser.add_argument('--getGraphs', default='OFF',
                    help='Whether to compute network graphs')
args = parser.parse_args()


############## SCENE SETUP ##################
scene = vp.canvas(width=700, height=700,
    center=vp.vector(0,0,0))
lamp = vp.local_light(pos=vp.vector(-1E10,1E10,-1E10),color=vp.color.white)

######### PHYSICAL PARAMETER SETUP #########
earth = vp.sphere(canvas=scene, pos=vp.vector(0,0,0), radius = 6.37E6, texture = vp.textures.earth)
earth.rotate(math.pi, axis=vp.vec(0,1,0))

earth.mass = 6E24
G = 6.673E-11
current_orbit = []
######## PLOT EQUATOR #####################################e
equator = []
for theta in np.arange(0,360,1):
    x = (earth.radius+100)*math.cos(math.radians(theta))
    y = (earth.radius+100)*math.sin(math.radians(theta))
    equator.append(vp.vector(x,0,y))
c = vp.curve(color=vp.color.blue, radius=100E2)
[c.append(x) for x in equator]

#All LEO satellites

# Initialise Phase 1 class with the following features
phase1 = Phase(phasenum=1,
                # On which canvas and around which object is the Phase plotted
                scene=scene,
                earth=earth,
                # Features of the Phase to plot
                phase_offset = Phases['Offset'][0],
                no_of_planes = Phases['Planes'][0],
                sats_per_plane = Phases['Sats per plane'][0],
                inclination = Phases['Inclination'][0],
                altitude = Phases['Altitude'][0])

# Plot the phase
phase1.phase()
# Orbit the satellites in the phase
phase1.orbit(run_rate=speed)



