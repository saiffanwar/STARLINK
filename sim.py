import math
from tkinter import *
from turtle import *
from vpython import *
import numpy as np

def polar2cart(r, theta, phi):
    return [
         r * math.sin(theta) * math.cos(phi),
         r * math.sin(theta) * math.sin(phi),
         r * math.cos(theta)
    ]

canvas(title='STARLINK',
     width=800, height=1200,
     center=vector(0,0,0), background=color.black)

earth_radius = 6371
earth_mass = 5.972*np.power(10,24)
earth = sphere(pos=vector(0,0,0), radius = earth_radius, texture=textures.earth)


def satellite(x,y,z):
    print(x,y,z)
    sphere(pos=vector(x,y,z), radius = 100, color = color.yellow)

# PHASE 1
phase1_altitude = 1150
phase1_mass = 250
# phase1_velocity = np.sqrt(((6.673E-11)*earth_mass)/earth_radius+phase1_altitude)

# sat1 = sphere(pos=vector(earth_radius+phase1_altitude, 0, 0), radius = 200, color = color.red)

# sat1.p = phase1_mass*vector(phase1_velocity,0,0)

# deltat = 0.01
# t =0

# while t<20:
#     sat1.pos = sat1.pos + (sat1.p/phase1_mass)*deltat
#     t += deltat
#     print(t)
#     rate(100)

phis = np.linspace(-(math.pi),(math.pi),20)
phis2 = np.linspace((math.pi),2*(math.pi),20)
print(phis)
for i in phis:
    print(i)
    for j in phis2:
        x, y, z = polar2cart(earth_radius+2000, j, i)
        satellite(x,y,z)