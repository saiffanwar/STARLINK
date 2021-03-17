import math
from tkinter import *
from turtle import *
from vpython import *
import numpy as np
import time
import threading
import threading
from geometry import *#polar2cart, polar2geo, cart2polar, cart2geo
from trackplot import plot_track
import pickle as pck
from matplotlib import pyplot as plt
import csv
# number of dp of accuracy for satellite postion. Higher dp leads to higher accuracy but slower build time
precision = 0

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


def plot_satellite(coords, velocity=0, colour=1):
    x, y, z = coords
    satellite = sphere(pos=vector(x,y,z), radius = (250*colour)*100, color=color.hsv_to_rgb(vector (0.5,1,0.8)))
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

def plane(object, no_of_sats, period):
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
    positions = []
    longitudes = []
    latitudes = []
    geopos = []
    while t<period:
        t = np.round(t, 2)
        pos=pos+velocity*dt
        force_gravity = -G*earth.mass*mass/(mag(pos-earth.pos)**2)*norm(pos-earth.pos)
        acceleration = force_gravity/mass
        velocity=velocity+acceleration*dt
        coords = [pos.x, pos.y, pos.z]
        if t in intervals[:-1]:
            positions.append([coords, velocity])
        longitude, latitude = cart2geo(pos.x, pos.y, pos.z)
        # print(latitude, longitude)
        longitudes.append(longitude)
        latitudes.append(latitude)
            # print('-------------------')
        t=t+dt
    col = 0
    for j in positions:
        col+=0.05
        pos = j[0]
        # print(j[0][0], j[0][1], j[0][2])
        geopos.append([j[0][0], j[0][1], j[0][2]])
        sat = plot_satellite(j[0], j[1])
        plane_sats.append(sat)
    # print(longitudes[1], latitudes[1])
    # print(longitudes[0:100], latitudes[0:100])

    # plot_track(latitudes, longitudes)
    with open('plane.csv','w+') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerows(geopos)
    # pck.dump([latitudes, longitudes], file)
    return plane_sats, latitudes, longitudes

def phase(no_of_planes, sats_per_plane, inclination, altitude):
    thetas = np.linspace(0,360,no_of_planes+1)
    thetas = thetas[:-1]
    sats = []
    planes = []
    period = (np.sqrt((4*(math.pi**2)*((altitude+earth.radius)**3))/(G*earth.mass)))
    for i in thetas:
        coords = polar2cart(earth_radius+altitude, rad(i), rad(inclination))
        # x, y, z = vpy2std(coords[0], coords[1], coords[2])
        x, y, z = coords
        speed = np.sqrt((G*earth.mass)/(earth_radius+altitude))
        if z <0:
            velocity = -speed*norm(hat(vector(1,0,(-x/z))))
        else:
            velocity = speed*norm(hat(vector(1,0,(-x/z))))
        initial_sat = plot_satellite(coords, velocity)
        initial_sat.visible = False
        plane_sats, latitudes, longitudes = plane(initial_sat,sats_per_plane, period)
        planes.append([latitudes, longitudes])
    
        for j in plane_sats:
            sats.append(j)
    plot_track(planes)
    return sats

#All LEO satellites

phase_sats1 = phase(32, 50, 53, 1150E3)
# print('part 1 plotted')
# phase_sats1 = phase_sats1[0::50]
# phase_sats2 = phase(32, 50, 53.8, 1100E3)
# print('part 2 plotted')
# # phase_sats2 = phase_sats2[0::50]
# phase_sats3 = phase(8, 50, 74, 1130E3)
# print('part 3 plotted')
# # phase_sats3 = phase_sats3[0::50]
# phase_sats4 = phase(5, 75, 81, 1275E3)
# print('part 4 plotted')
# # phase_sats4 = phase_sats4[0::75]
# phase_sats5 = phase(6, 75, 70, 1325E3)
# print('part 5 plotted')
# phase_sats5 = phase_sats5[0::75]

# threading.Thread(target=orbit, args=(phase_sats1, 1150E3)).start()
# threading.Thread(target=orbit, args=(phase_sats2, 1100E3)).start()
# threading.Thread(target=orbit, args=(phase_sats3, 1130E3)).start()
# threading.Thread(target=orbit, args=(phase_sats4, 1275E3)).start()
# threading.Thread(target=orbit, args=(phase_sats5, 1325E3)).start()

# phase_sats1 = phase(1, 1, 140, 1150E3)
# orbit(phase_sats1, 1150E3, 5) 


def coord_plane(theta, phi):
    altitude = 1150E3
    print(earth_radius+altitude, theta*math.pi/180, phi*math.pi/180) 
    coords = polar2cart(earth_radius+altitude, theta*math.pi/180, phi*math.pi/180)
    print(std2vpy(coords[0], coords[1], coords[2],inverse=1)) 
    r, phi, theta = cart2polar(coords[0], coords[1], coords[2])
    print(r, phi*180/math.pi, theta*180/math.pi) 
    longitude, latitude = cart2geo(coords[0], coords[1], coords[2])
    # longitude, latitude = polar2geo(r, phi, theta)
    print(latitude, longitude) 
    # polar2geo(earth_radius+1150E3, theta*math.pi/180, phi*math.pi/180)
    x, y, z = coords
    speed = np.sqrt((G*earth.mass)/(earth_radius+altitude))
    if z <0:
        velocity = -speed*norm(hat(vector(1,0,(-x/z))))
    else:
        velocity = speed*norm(hat(vector(1,0,(-x/z))))
    # print(coords)
    initial_sat = plot_satellite(coords, velocity, 2)
    # initial_sat.visible = False
    period = (np.sqrt((4*(math.pi**2)*((altitude+earth.radius)**3))/(G*earth.mass)))
    plane_sats = plane(initial_sat,20, period)


coord_plane(0, 53)

# coord_plane(0,50)

# polar2geo(1150E3, 270,45)

# cart2geo()