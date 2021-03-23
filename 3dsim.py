import math
from tkinter import *
from turtle import *
from vpython import *
import numpy as np
import time
import threading
import threading
from geometry import *
import pickle as pck
from matplotlib import pyplot as plt
import csv
# from app import *



# number of dp of accuracy for satellite postion. Higher dp leads to higher accuracy but slower build time
precision = -1

############## SCENE SETUP ##################
canvas(title='STARLINK',
     width=1200, height=1200,
     center=vector(0,0,0), background=color.black)
# distant_light(direction=vector(-1E10,1E10,-1E10), color=color.white)
# distant_light(direction=vector(1E10,-0,1E10), color=color.white)
lamp = local_light(pos=vector(-1E10,1E10,-1E10),color=color.white)
lamp = local_light(pos=vector(1E10,-1E10,-0),color=color.white)

######### PHYSICAL PARAMETER SETUP #########
earth_radius = 6.37E6
earth = sphere(pos=vector(0,0,0), radius = earth_radius, texture = textures.earth)
earth.mass = 6E24
G = 6.673E-11


def plot_satellite(coords, velocity=0):
    x, y, z = coords
    satellite = sphere(pos=vector(x,y,z), radius = 250E2, color=color.red)

    # satellite = box(pos=vector(x,y,z), width = 250E2, height = 250E2, length = 250E2, color=color.white)

    satellite.mass = 250
    satellite.velocity = velocity
    satellite.acceleration = vector(0,0,0)
    satellite.orbit = curve(color=color.green, radius=10E3)    

    return satellite



def orbit(sats, altitude, run_rate=1):
    force_gravity = vector(0,0,0)
    t = 0
    dt = 1
    period = (np.sqrt((4*(math.pi**2)*((altitude+earth.radius)**3))/(G*earth.mass)))
    # while t<period:
    while True:
        # print(t)
        for object in sats:
            rate(100*len(sats)*run_rate)
            force_gravity = -G*earth.mass*object.mass/(mag(object.pos-earth.pos)**2)*norm(object.pos-earth.pos)
            object.acceleration = force_gravity/object.mass

            object.velocity=object.velocity+object.acceleration*dt
            object.pos=object.pos+object.velocity*dt

            object.orbit.append(pos=object.pos)
        t=t+dt

def plane(object, no_of_sats, period, plane_number, total_planes):
    plane_sats = []
    force_gravity = vector(0,0,0)
    t = 0
    dt = 10**(-precision)
    pos = object.pos
    velocity = object.velocity
    acceleration = object.acceleration
    mass = object.mass
    coords = [pos.x, pos.y, pos.z]
    intervals = np.around(np.linspace(0,period,no_of_sats+1), precision)
    intervals = [interval+(20*plane_number) for interval in intervals]
    positions = []
    latitudes = []
    longitudes = []
    starting_positions = []

    while t<period+20*total_planes:
        t = np.round(t, 2)
        pos=pos+velocity*dt
        force_gravity = -G*earth.mass*mass/(mag(pos-earth.pos)**2)*norm(pos-earth.pos)
        acceleration = force_gravity/mass
        velocity=velocity+acceleration*dt
        coords = [pos.x, pos.y, pos.z]
        longitude, latitude = cart2geo(pos.x, pos.y, pos.z)
        longitudes.append(longitude)
        latitudes.append(latitude)
        if t in intervals[:-1]:
            # print(velocity)
            positions.append([coords, velocity])
            starting_positions.append([longitude, latitude])
        t=t+dt
    for j in positions:
        pos = j[0]
        sat = plot_satellite(j[0], j[1])
        plane_sats.append(sat)
    return plane_sats, longitudes, latitudes, starting_positions

def phase(no_of_planes, sats_per_plane, inclination, altitude, section):
    thetas = np.linspace(0,360,no_of_planes+1)
    thetas = thetas[:-1]
    sats = []
    all_latitudes = []
    all_longitudes = []
    all_initial_pos = []
    period = (np.sqrt((4*(math.pi**2)*((altitude+earth.radius)**3))/(G*earth.mass)))
    satellite_separation = period/sats_per_plane

    for i in range(0,len(thetas)):
        coords = polar2cart(earth_radius+altitude, rad(thetas[i]), rad(inclination))
        x, y, z = coords
        speed = np.sqrt((G*earth.mass)/(earth_radius+altitude))
        if z <0:
            velocity = -speed*norm(hat(vector(1,0,(-x/z))))
        else:
            velocity = speed*norm(hat(vector(1,0,(-x/z))))
        initial_sat = plot_satellite(coords, velocity)
        initial_sat.visible = False
        plane_sats, longitudes, latitudes, starting_positions = plane(initial_sat,sats_per_plane, period, i, no_of_planes)
        all_latitudes.append(latitudes)
        all_longitudes.append(longitudes) 
        all_initial_pos.append(starting_positions)
        
        for j in plane_sats:
            sats.append(j)
            
    with open('data/planes'+str(section)+'.pck', 'wb') as f:
        pck.dump([all_longitudes, all_latitudes, section, all_initial_pos], f)
    return sats

#All LEO satellites

phase_sats1 = phase(32, 50, 53, 1150E3, 1)
phase_sats2 = phase(32, 50, 53.8, 1100E3, 2)
phase_sats3 = phase(8, 50, 74, 1130E3, 3)
phase_sats4 = phase(5, 75, 81, 1275E3, 4)
phase_sats5 = phase(6, 75, 70, 1325E3, 5)

# threading.Thread(target=orbit, args=(phase_sats1, 1150E3)).start()
# threading.Thread(target=orbit, args=(phase_sats2, 1100E3)).start()
# threading.Thread(target=orbit, args=(phase_sats3, 1130E3)).start()
# threading.Thread(target=orbit, args=(phase_sats4, 1275E3)).start()
# threading.Thread(target=orbit, args=(phase_sats5, 1325E3)).start()
