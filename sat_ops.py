import math
from tkinter import *
from turtle import *
from pprint import pprint
from sim_utils import colourdict, speed, calcGCR

from numpy.lib.utils import source
from vpython import *
import numpy as np
import time
import threading
from geometry import rad, deg, cart2geo, cart2polar, polar2cart
# from sim_utils import Phases, colourdict, speed, calcGCR
import pickle as pck
from network import createNetworkGraph, calcPath, plotShortestPath, plot_3d_edges
# from graphcomp import compute_graphs
# number of dp of accuracy for satellite postion. Higher dp leads to higher accuracy but slower build time
precision = -1
G = 6.673E-11


def plot_satellite(coords, scene, velocity=0, rgb=[255, 0, 0]):
    x, y, z = coords
    satellite = sphere(canvas=scene, pos=vector(x,y,z), radius = 1000E2, color=vector(rgb[0]/255, rgb[1]/255, rgb[2]/255))
    satellite.mass = 250
    satellite.velocity = velocity
    satellite.acceleration = vector(0,0,0)
    satellite.orbit = curve(canvas=scene, color=color.green, radius=10E3)    
    satellite.geopos = [x for x in cart2geo(coords[0], coords[1], coords[2])]

    return satellite




class Phase():
    def __init__(self, 
                phasenum, 
                scene, 
                earth,
                phase_offset, 
                no_of_planes, 
                sats_per_plane, 
                inclination, 
                altitude) -> None:
        self.phasenum = phasenum
        self.phase_offset = phase_offset
        self.scene = scene
        self.earth = earth
        self.no_of_planes = no_of_planes
        self.sats_per_plane = sats_per_plane
        self.inclination = inclination
        self.altitude = altitude
        self.PhaseSats = []

    def plane(self, init_sat, period, plane_number):
        plane_sats = []
        offset = self.phase_offset/self.no_of_planes * (period/self.sats_per_plane)
        force_gravity = vector(0,0,0)
        t = 0
        dt = 10**(-precision)
        pos = init_sat.pos
        velocity = init_sat.velocity
        acceleration = init_sat.acceleration
        mass = init_sat.mass
        coords = [pos.x, pos.y, pos.z]
        intervals = np.around(np.linspace(0+(offset*plane_number),period+(offset*plane_number),self.sats_per_plane+1), precision)[:-1]
        positions = []

        orbit = []
        while t<period+offset*self.no_of_planes:
            t = np.round(t, 2)
            pos=pos+velocity*dt
            force_gravity = -G*self.earth.mass*mass/(mag(pos-self.earth.pos)**2)*norm(pos-self.earth.pos)
            acceleration = force_gravity/mass
            velocity=velocity+acceleration*dt
            coords = [pos.x, pos.y, pos.z]
            orbit.append(pos)
            if t in intervals:
                positions.append([coords, velocity])
            t=t+dt
        for satnum, j in list(enumerate(positions)):
            pos = j[0]
            sat = plot_satellite(j[0], self.scene, j[1], colourdict[self.phasenum][1])
            curve(vec(0,0,0), j[0])
            sat.geopos = [x for x in cart2geo(coords[0], coords[1], coords[2])]
            plane_sats.append(sat)
            sat.id = [plane_number, satnum]
        c = curve(color=color.green, radius=100E2)
        [c.append(x) for x in orbit]
        return plane_sats


    def phase(self):

        thetas = np.linspace(0,360,self.no_of_planes+1)[:-1]
        period = (np.sqrt((4*(math.pi**2)*((self.altitude+self.earth.radius)**3))/(G*self.earth.mass)))
        satellite_separation = period/self.sats_per_plane

        for i in range(0,len(thetas)):
            coords = polar2cart(self.earth.radius+self.altitude, rad(thetas[i]), rad(90-self.inclination))
            x, y, z = coords
            speed = np.sqrt((G*self.earth.mass)/(self.earth.radius+self.altitude))
            if z <0:
                velocity = -speed*norm(hat(vector(1,0,(-x/z))))
            else:
                velocity = speed*norm(hat(vector(1,0,(-x/z))))
            initial_sat = plot_satellite(coords, self.scene, velocity)
            initial_sat.visible = False
            plane_sats = self.plane(initial_sat, period, i)
            self.PhaseSats = np.array(np.append(self.PhaseSats, plane_sats)).flatten()
            all_initial_pos = [[s.pos.x, s.pos.y, s.pos.z] for s in self.PhaseSats]
        t=0
        with open('data/'+str(int(self.altitude/1E3))+'/curr_positions.pck', 'wb') as f:
            pck.dump([t,all_initial_pos], f)

    def new_pos(self, sat, dt):
        force_gravity = -G*self.earth.mass*sat.mass/(mag(sat.pos-self.earth.pos)**2)*norm(sat.pos-self.earth.pos)
        sat.acceleration = force_gravity/sat.mass
        sat.velocity=sat.velocity+sat.acceleration*dt
        pos =sat.pos+sat.velocity*dt
        sat.pos = pos
        sat.geopos = [x for x in cart2geo(pos[0], pos[1], pos[2])]

        return sat

    def orbit(self, time_limit=100000, run_rate=1):
        t = 0
        dt = 1
        orbit = []
        curr_positions = []
        pathLengths = []
        oldedges = []
        all_sats = np.array(self.PhaseSats).flatten()
        for i, sat in list(enumerate(all_sats)):
            self.new_pos(sat, dt)
            pos = sat.pos
            curr_positions.append([pos.x, pos.y, pos.z])
            orbit.append([t,[pos.x, pos.y, pos.z]])
        t=t+dt
        with open('data/'+str(int(self.altitude/1E3))+'/curr_positions.pck', 'wb') as f:
            pck.dump([t,curr_positions], f)


        while True:
            self.earth.rotate(rad(1/240), axis=vec(0,1,0))
            # Computes the graph of the current static network and stores it in a dict with the timestamp.
            rate(100*len(self.PhaseSats)*run_rate)
            curr_positions = []
            all_sats = np.array(self.PhaseSats).flatten()
            for i, sat in list(enumerate(all_sats)):
                self.new_pos(sat, dt)
                curr_positions.append([sat.pos.x, sat.pos.y, sat.pos.z])
                orbit.append([t,[sat.pos.x, sat.pos.y, sat.pos.z]])

            with open('data/'+str(int(self.altitude/1E3))+'/curr_positions.pck', 'wb') as f:
                pck.dump([t,curr_positions], f)

            # Graph, nodes = createNetworkGraph(self, t)
            # edges = plot_3d_edges(nodes, Graph, phasenum)
            # plot_3d_edges(nodes, Graph)

            # PATHFINDING
            # shortest_path, distance, Graph = calcPath(self.phasenum, t, Graph, curr_positions, nodes)
            # oldedges = plotShortestPath(shortest_path, nodes, oldedges)

            # sourceCartPos = nodes[shortest_path[0]]
            # sourceGeoPos = cart2geo(sourceCartPos[0], sourceCartPos[1], sourceCartPos[2])
            # destCartPos = nodes[shortest_path[-1]]
            # destGeoPos = cart2geo(destCartPos[0], destCartPos[1], destCartPos[2])
            # gcr = calcGCR(sourceGeoPos, destGeoPos)

            # pathLengths.append([t,[distance, gcr]])
            # with open('data/'+str(int(self.altitude/1E3))+'/pathLengths.pck', 'wb') as f:
            #     pck.dump(pathLengths, f)
            # time.sleep(1)

            time.sleep(1/speed)
            t=t+dt
            # if t%1000==0:
            #     print(t)    
            if t > time_limit:
                break

        # with open('data/'+str(int(self.altitude/1E3))+'/orbit.pck', 'wb') as f:
        #     pck.dump(orbit, f)
        print('files saved')