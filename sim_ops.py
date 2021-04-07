import math
from tkinter import *
from turtle import *
from vpython import *
import numpy as np
import time
import threading
from geometry import *
import pickle as pck
import csv
# from flatsim import *
import pandas as pd


# number of dp of accuracy for satellite postion. Higher dp leads to higher accuracy but slower build time
precision = -1


colourdict = {1 : ['red', [255, 0, 0] ], 
                2 : ['green', [0, 255, 0]], 
                3: ['orange', [255, 165, 0]], 
                4: ['purple', [128, 0, 128]], 
                5: ['hotpink', [255, 105, 180]]}

############## SCENE SETUP ##################
canvas(title='STARLINK',
    width=1000, height=1500,
    center=vector(0,0,0), background=vector(40/255, 44/255, 51/255))
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
    satellite = sphere(pos=vector(x,y,z), radius = 150E2, color=vector(rgb[0]/255, rgb[1]/255, rgb[2]/255))
    satellite.mass = 250
    satellite.velocity = velocity
    satellite.acceleration = vector(0,0,0)
    satellite.orbit = curve(color=color.green, radius=10E3)    

    return satellite

def orbit(sats, altitude, deployment, sats_per_plane, no_of_planes, run_rate=1):
    force_gravity = vector(0,0,0)
    t = 0
    dt = 1
    period = (np.sqrt((4*(math.pi**2)*((altitude+earth.radius)**3))/(G*earth.mass)))
    plane = [pos for pos in sats ]
    while True:
        # earth.rotate(rad(1/240), axis=vec(0,1,0))
        # print(t)
        rate(100*len(sats)*run_rate)
        plane_positions = [[no_of_planes, sats_per_plane]]
        for i, object in zip(np.arange(0,len(plane)), plane):
            new_pos(object, dt)
            pos = object.pos
            plane_positions.append([pos.x, pos.y, pos.z])
        with open('data/positions'+str(deployment)+'.pck', 'wb') as f:
            pck.dump(plane_positions, f)
        
        # time.sleep(1)
        t=t+dt

def new_pos(object, dt):
    force_gravity = -G*earth.mass*object.mass/(mag(object.pos-earth.pos)**2)*norm(object.pos-earth.pos)
    object.acceleration = force_gravity/object.mass

    object.velocity=object.velocity+object.acceleration*dt
    pos =object.pos+object.velocity*dt
    # Rotate the theta position by 1/240 deg (earths rotation per second)
    r, theta, phi = cart2polar(pos.x, pos.y, pos.z)
    rotated_position = polar2cart(r, rotate_orbit(theta, pos.x), phi)
    object.pos = vec(rotated_position[0], rotated_position[1], rotated_position[2])
    # object.orbit.append(pos=object.pos)
    # geo_pos = cart2geo(pos.x, pos.y, pos.z)
    # current_orbit.append([geo_pos[0], geo_pos[1]])
    # print(current_orbit)
    # with open('data/orbit.pck', 'wb') as f:
    #         pck.dump(current_orbit, f)
    return object

def initial_plane(object, no_of_sats, period, plane_number, total_planes, section):
    plane_sats = []
    phase_offset = 5/32 * (period/no_of_sats)
    force_gravity = vector(0,0,0)
    t = 0
    dt = 10**(-precision)
    pos = object.pos
    velocity = object.velocity
    acceleration = object.acceleration
    mass = object.mass
    coords = [pos.x, pos.y, pos.z]
    intervals = np.around(np.linspace(0+(phase_offset*plane_number),period+(phase_offset*plane_number),no_of_sats+1), precision)[:-1]
    positions = []
    latitudes = []
    longitudes = []
    starting_positions = []
    orbit = []
    while t<period+phase_offset*total_planes:
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
            # print(velocity)
            positions.append([coords, velocity])
            starting_positions.append([longitude, latitude])
        t=t+dt
    for j in positions:
        pos = j[0]
        sat = plot_satellite(j[0], j[1], colourdict[section][1])
        plane_sats.append(sat)
    # c = curve(color=vector(colourdict[section][1][0]/255, colourdict[section][1][1]/255, colourdict[section][1][2]/255), radius=50E2)
    # [c.append(x) for x in orbit]
    return plane_sats, longitudes, latitudes, starting_positions

def phase(no_of_planes, sats_per_plane, inclination, altitude, section):
    thetas = np.linspace(0,360,no_of_planes+1)
    if section ==2:
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
        plane_sats, longitudes, latitudes, starting_positions = initial_plane(initial_sat,sats_per_plane, period, i, no_of_planes, section)
        all_latitudes.append(latitudes)
        all_longitudes.append(longitudes) 
        all_initial_pos.append(starting_positions)
        
        for j in plane_sats:
            sats.append(j)
            
    with open('data/planes'+str(section)+'.pck', 'wb') as f:
        pck.dump([all_longitudes, all_latitudes, section, all_initial_pos], f)
    threading.Thread(target=orbit, args=(sats, altitude, section, sats_per_plane, no_of_planes)).start()
    return sats

