import math
from tkinter import *
from turtle import *
from vpython import *
import numpy as np
import time
import threading
from geometry import rad, deg, cart2geo, cart2polar, polar2cart
from sim_utils import rotate_orbit, Phases, colourdict, speed
import pickle as pck
from graphcomp import compute_graphs
# number of dp of accuracy for satellite postion. Higher dp leads to higher accuracy but slower build time
precision = -1



############## SCENE SETUP ##################
canvas(title='STARLINK',
    width=1000, height=1500,
    center=vector(0,0,0))
lamp = local_light(pos=vector(-1E10,1E10,-1E10),color=color.white)

######### PHYSICAL PARAMETER SETUP #########
earth_radius = 6.37E6
earth = sphere(pos=vector(0,0,0), radius = earth_radius, texture = textures.earth)
earth.mass = 6E24
G = 6.673E-11
current_orbit = []
######## PLOT EQUATOR #####################################e
equator = []
for theta in np.arange(0,360,1):
    x = (earth_radius+100)*math.cos(rad(theta))
    y = (earth_radius+100)*math.sin(rad(theta))
    equator.append(vector(x,0,y))
c = curve(color=color.blue, radius=100E2)
[c.append(x) for x in equator]

def plot_satellite(coords, velocity=0, rgb=[255, 0, 0]):
    x, y, z = coords
    satellite = sphere(pos=vector(x,y,z), radius = 1000E2, color=vector(rgb[0]/255, rgb[1]/255, rgb[2]/255))
    satellite.mass = 250
    satellite.velocity = velocity
    satellite.acceleration = vector(0,0,0)
    satellite.orbit = curve(color=color.green, radius=10E3)    

    return satellite

def orbit(sats, phasenum, time_limit=1000000000, getGraphs=False, run_rate=1):
    print('Starting orbit')
    no_of_planes = Phases['Planes'][phasenum-1]
    sats_per_plane = Phases['Sats per plane'][phasenum-1]
    altitude = Phases['Altitude'][phasenum-1]

    force_gravity = vector(0,0,0)
    t = 0
    dt = 1
    period = (np.sqrt((4*(math.pi**2)*((altitude+earth.radius)**3))/(G*earth.mass)))
    plane = [pos for pos in sats ]

    positions = {}
    orbit = []
    plane_positions = []
    for i, object in zip(np.arange(0,len(plane)), plane):
        new_pos(object, dt)
        pos = object.pos
        plane_positions.append([pos.x, pos.y, pos.z])
        orbit.append([t,[pos.x, pos.y, pos.z]])
    positions[str(t)] = plane_positions
    with open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/plane_positions.pck', 'wb') as f:
        pck.dump([t,plane_positions], f)
    while True:
        earth.rotate(rad(1/240), axis=vec(0,1,0))
        # Computes the graph of the current static network and stores it in a dict with the timestamp.
        rate(100*len(sats)*run_rate)
        plane_positions = []
        for i, object in zip(np.arange(0,len(plane)), plane):
            new_pos(object, dt)
            pos = object.pos
            plane_positions.append([pos.x, pos.y, pos.z])
            orbit.append([t,[pos.x, pos.y, pos.z]])
        time.sleep(1 /speed)
        t=t+dt
        if t%1000==0:
            print(t)    
        if t > time_limit:
            break
        positions[str(t)] = plane_positions
        with open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/plane_positions.pck', 'wb') as f:
            pck.dump([t,plane_positions], f)
    print(t)
    with open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/positions.pck', 'wb') as f:
        pck.dump(positions, f)
    with open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/orbit.pck', 'wb') as f:
        pck.dump(orbit, f)
    print('files saved')
    if getGraphs:
        compute_graphs(time_limit)        


def new_pos(object, dt):
    force_gravity = -G*earth.mass*object.mass/(mag(object.pos-earth.pos)**2)*norm(object.pos-earth.pos)
    object.acceleration = force_gravity/object.mass
    object.velocity=object.velocity+object.acceleration*dt
    pos =object.pos+object.velocity*dt
    r, theta, phi = cart2polar(pos.x, pos.y, pos.z)
    object.pos = pos

    return object

def initial_plane(object, no_of_sats, period, plane_number, total_planes, phasenum, phase_offset):
    plane_sats = []
    offset = phase_offset/total_planes * (period/no_of_sats)
    force_gravity = vector(0,0,0)
    t = 0
    dt = 10**(-precision)
    pos = object.pos
    velocity = object.velocity
    acceleration = object.acceleration
    mass = object.mass
    coords = [pos.x, pos.y, pos.z]
    intervals = np.around(np.linspace(0+(offset*plane_number),period+(offset*plane_number),no_of_sats+1), precision)[:-1]
    positions = []
    latitudes = []
    longitudes = []
    starting_positions = []
    orbit = []
    while t<period+offset*total_planes:
        t = np.round(t, 2)
        pos=pos+velocity*dt
        force_gravity = -G*earth.mass*mass/(mag(pos-earth.pos)**2)*norm(pos-earth.pos)
        acceleration = force_gravity/mass
        velocity=velocity+acceleration*dt
        coords = [pos.x, pos.y, pos.z]
        orbit.append(pos)
        longitude, latitude = cart2geo(pos.x, pos.y, pos.z)
        longitudes.append(longitude)
        latitudes.append(latitude)
        if t in intervals:
            positions.append([coords, velocity])
            starting_positions.append(coords)
        t=t+dt
    for j in positions:
        pos = j[0]
        sat = plot_satellite(j[0], j[1], colourdict[phasenum][1])

        plane_sats.append(sat)
    c = curve(color=color.green, radius=100E2)
    [c.append(x) for x in orbit]
    return plane_sats, longitudes, latitudes, starting_positions

def phase(phasenum, phase_offset=Phases['Offset'][0]):
    no_of_planes = Phases['Planes'][phasenum-1]
    sats_per_plane = Phases['Sats per plane'][phasenum-1]
    inclination = Phases['Inclination'][phasenum-1]
    altitude = Phases['Altitude'][phasenum-1]

    thetas = np.linspace(0,360,no_of_planes+1)
    if phasenum ==2:
        thetas = np.linspace((360/no_of_planes)/2,360+ (360/no_of_planes)/2,no_of_planes+1)
    thetas = thetas[:-1]
    sats = []
    all_latitudes = []
    all_longitudes = []
    all_initial_pos = []
    period = (np.sqrt((4*(math.pi**2)*((altitude+earth.radius)**3))/(G*earth.mass)))
    satellite_separation = period/sats_per_plane

    for i in range(0,len(thetas)):
        coords = polar2cart(earth_radius+altitude, rad(thetas[i]), rad(90-inclination))
        x, y, z = coords
        speed = np.sqrt((G*earth.mass)/(earth_radius+altitude))
        if z <0:
            velocity = -speed*norm(hat(vector(1,0,(-x/z))))
        else:
            velocity = speed*norm(hat(vector(1,0,(-x/z))))
        initial_sat = plot_satellite(coords, velocity)
        initial_sat.visible = False
        plane_sats, longitudes, latitudes, starting_positions = initial_plane(initial_sat,sats_per_plane, period, i, no_of_planes, phasenum, phase_offset)
        all_latitudes.append(latitudes)
        all_longitudes.append(longitudes) 
        [all_initial_pos.append(i) for i in starting_positions]
        
        for j in plane_sats:
            sats.append(j)
    t=0
    with open('data/plane_positions'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'.pck', 'wb') as f:
            pck.dump([t,all_initial_pos], f)
    return sats

    
