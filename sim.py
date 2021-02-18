import math
from tkinter import *
from turtle import *
from vpython import *
import numpy as np
import time
import threading

def polar2cart(r, theta, phi): 
    z = r * math.sin(phi) * math.cos(theta)
    x = r * math.sin(phi) * math.sin(theta)
    y = r * math.cos(phi)
    return [x, y, z]

canvas(title='STARLINK',
     width=1200, height=1200,
     center=vector(0,0,0), background=color.black)
# distant_light(direction=vector(1E10,1E10,1E10), color=color.blue)

earth_radius = 6.37E6
earth = sphere(pos=vector(0,0,0), radius = earth_radius, texture = textures.earth)
earth.mass = 6E24
G = 6.673E-11

def plot_satellite(coords, velocity):
    x, y, z = coords
    satellite = sphere(pos=vector(x,y,z), radius = 500E2)
    satellite.mass = 250
    satellite.velocity = velocity
    satellite.acceleration = vector(0,0,0)
    satellite.orbit = curve(color=color.green, radius=10E3)    

    return satellite

def orbit(sats):
    force_gravity = vector(0,0,0)
    force_satellite = vector(0,0,0)
    t = 0
    dt = 1
    while t<6475:
        # print(t)
        for object in sats:
            rate(10000)
            force_gravity = -G*earth.mass*object.mass/(mag(object.pos-earth.pos)**2)*norm(object.pos-earth.pos)
            # if t%1000 == 0:
            #     print(t, object.velocity, object.pos) 
            #Update the acceleration, velocity, and postion of the satellite
            object.acceleration = force_gravity/object.mass

            object.velocity=object.velocity+object.acceleration*dt
            object.pos=object.pos+object.velocity*dt

            object.orbit.append(pos=object.pos)
        t=t+dt

def plane(object, no_of_sats):
    plane_sats = []
    force_gravity = vector(0,0,0)
    force_satellite = vector(0,0,0)
    t = 0
    dt = 0.1
    intervals = np.linspace(0,6475,no_of_sats+1)
    pos = object.pos
    velocity = object.velocity
    acceleration = object.acceleration
    mass = object.mass
    coords = [pos.x, pos.y, pos.z]
    positions = [[coords, velocity]]

    while t<6475:
        force_gravity = -G*earth.mass*mass/(mag(pos-earth.pos)**2)*norm(pos-earth.pos)
        acceleration = force_gravity/mass
        velocity=velocity+acceleration*dt
        pos=pos+velocity*dt
        if np.round(t,1) in intervals[:-1]:
            coords = [pos.x, pos.y, pos.z]
            positions.append([coords, velocity])
        t=t+dt

    for j in positions:
        pos = j[0]
        sat = plot_satellite(j[0], j[1])
        plane_sats.append(sat)

    return plane_sats

# PHASE 1
thetas = np.linspace(0,360,33)
thetas = thetas[:-1]


inclination = 53
sats = []
iter=0
y_old = 0
for i in thetas:
    coords = polar2cart(earth_radius+1150E3, i*math.pi/180, (inclination/180)*math.pi)
    x, y, z = coords
    if z <0:
        velocity = -7.3E3*norm(hat(vector(1,0,(-x/z))))
    else:
        velocity = 7.3E3*norm(hat(vector(1,0,(-x/z))))
    initial_sat = plot_satellite(coords, velocity)
    plane_sats = plane(initial_sat,50)
    for j in plane_sats:
        sats.append(j)

# orbit(sats)

