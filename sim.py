import math
from tkinter import *
from turtle import *
from vpython import *
import numpy as np
import time
import threading
import threading

# number of dp of accuracy for satellite postion. Higher dp leads to higher accuracy but slower build time
precision = 1

def polar2cart(r, theta, phi): 
    z = r * math.sin(phi) * math.cos(theta)
    x = r * math.sin(phi) * math.sin(theta)
    y = r * math.cos(phi)
    return [x, y, z]

canvas(title='STARLINK',
     width=1200, height=1200,
     center=vector(0,0,0), background=color.black)
# distant_light(direction=vector(-1E10,1E10,-1E10), color=color.white)
# distant_light(direction=vector(1E10,-0,1E10), color=color.white)
lamp = local_light(pos=vector(-1E10,1E10,-1E10),color=color.white)
lamp = local_light(pos=vector(1E10,-1E10,-0),color=color.white)


earth_radius = 6.37E6
earth = sphere(pos=vector(0,0,0), radius = earth_radius, texture = textures.earth)
earth.mass = 6E24
G = 6.673E-11

def plot_satellite(coords, velocity):
    x, y, z = coords
    # satellite = sphere(pos=vector(x,y,z), radius = 250E2, color=color.white)
    satellite = box(pos=vector(x,y,z), width = 250E2, height = 250E2, length = 250E2, color=color.white)

    satellite.mass = 250
    satellite.velocity = velocity
    satellite.acceleration = vector(0,0,0)
    satellite.orbit = curve(color=color.green, radius=10E3)    

    return satellite

def orbit(sats, altitude):
    force_gravity = vector(0,0,0)
    t = 0
    dt = 1
    period = (np.sqrt((4*(math.pi**2)*((altitude+earth.radius)**3))/(G*earth.mass)))
    # while t<period:
    while True:
        # print(t)
        for object in sats:
            rate(100*len(sats))
            force_gravity = -G*earth.mass*object.mass/(mag(object.pos-earth.pos)**2)*norm(object.pos-earth.pos)
            object.acceleration = force_gravity/object.mass

            object.velocity=object.velocity+object.acceleration*dt
            object.pos=object.pos+object.velocity*dt

            # object.orbit.append(pos=object.pos)
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
    while t<period:
        t = np.round(t, 2)
        pos=pos+velocity*dt
        force_gravity = -G*earth.mass*mass/(mag(pos-earth.pos)**2)*norm(pos-earth.pos)
        acceleration = force_gravity/mass
        velocity=velocity+acceleration*dt
        if t in intervals[:-1]:
            coords = [pos.x, pos.y, pos.z]
            positions.append([coords, velocity])
        t=t+dt
    for j in positions:
        pos = j[0]
        sat = plot_satellite(j[0], j[1])
        plane_sats.append(sat)

    return plane_sats

def phase(no_of_planes, sats_per_plane, inclination, altitude):
    thetas = np.linspace(0,360,no_of_planes+1)
    thetas = thetas[:-1]
    sats = []
    period = (np.sqrt((4*(math.pi**2)*((altitude+earth.radius)**3))/(G*earth.mass)))
    for i in thetas:
        coords = polar2cart(earth_radius+altitude, i*math.pi/180, (inclination/180)*math.pi)
        x, y, z = coords
        speed = np.sqrt((G*earth.mass)/(earth_radius+altitude))
        if z <0:
            velocity = -speed*norm(hat(vector(1,0,(-x/z))))
        else:
            velocity = speed*norm(hat(vector(1,0,(-x/z))))
        initial_sat = plot_satellite(coords, velocity)
        initial_sat.visible = False
        plane_sats = plane(initial_sat,sats_per_plane, period)
        for j in plane_sats:
            sats.append(j)
    return sats

#All LEO satellites

phase_sats1 = phase(32, 50, 53, 1150E3)
print('part 1 plotted')
# phase_sats1 = phase_sats1[0::50]
phase_sats2 = phase(32, 50, 53.8, 1100E3)
print('part 2 plotted')
# phase_sats2 = phase_sats2[0::50]
phase_sats3 = phase(8, 50, 74, 1130E3)
print('part 3 plotted')
# phase_sats3 = phase_sats3[0::50]
phase_sats4 = phase(5, 75, 81, 1275E3)
print('part 4 plotted')
# phase_sats4 = phase_sats4[0::75]
phase_sats5 = phase(6, 75, 70, 1325E3)
print('part 5 plotted')
# phase_sats5 = phase_sats5[0::75]

threading.Thread(target=orbit, args=(phase_sats1, 1150E3)).start()
threading.Thread(target=orbit, args=(phase_sats2, 1100E3)).start()
threading.Thread(target=orbit, args=(phase_sats3, 1130E3)).start()
threading.Thread(target=orbit, args=(phase_sats4, 1275E3)).start()
threading.Thread(target=orbit, args=(phase_sats5, 1325E3)).start()



