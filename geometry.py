import math
import numpy as np
from tkinter import *
from turtle import *
from vpython import *

# VPython's coordinate axis are wrong according to standard practice.
# This function rearranges the coordinates to comply with the library.

def rad(x):
    return (x*math.pi/180)

def deg(x):
    return (x*180/math.pi)
def std2vpy(old_x,old_y,old_z, inverse=0):
    new_x = old_y
    new_y = old_z
    new_z = old_x
    if (inverse == 1):
        new_x = old_z
        new_y = old_x
        new_z = old_y 
    return new_x, new_y, new_z

# def polar2cart(r, theta, phi, inverse=0):
#     x = r * math.sin(theta) * math.cos(phi)
#     y = r * math.sin(theta) * math.sin(phi)
#     z = r * math.cos(phi)
#     print(x,y,z)
#     return vpy2std(x,y,z,inverse=0)

def polar2cart(r, theta, phi): 
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)

    x,y,z = std2vpy(x,y,z)
    if (phi > math.pi/2):
        x = -x
        z = -z
    return [x, y, z]
    
def polar2geo(r, theta, phi, x):
    # theta = theta*180/math.pi
    # phi = phi*180/math.pi
    # print(r, deg(theta), deg(phi))
    # x,y,z = polar2cart(r, theta, phi)
    if (x < 0):
        if (theta <= 0):
            latitude = theta + math.pi
            longitude = -(math.pi/2 - phi)
        elif (theta > 0):
            latitude = (theta - math.pi)
            longitude = (math.pi/2 - phi)
        # latitude = theta + math.pi
    else:
        latitude = theta
        if (theta<=0):
            longitude = -(math.pi/2 - phi)
        else:
            longitude = (math.pi/2 - phi)

        
    # if (phi >= 90):
    #     longitude = phi - 180
    # else:

    return deg(longitude), deg(latitude)
    
def cart2polar(x, y, z):
    x,y,z = std2vpy(x,y,z,inverse=1)
    # print(x,y,z)
    r = np.sqrt((x**2)+(y**2)+(z**2))

    phi = np.arccos(z/r)
    
    # if (phi > math.pi):
    #     theta = -np.arctan(y/x)
    # else:
    theta = np.arctan(y/x)
    # print('cart2polar: ', r, theta, phi)
    return r, theta, phi

def cart2geo(x, y, z):
    # x,y,z = std2vpy(x,y,z,inverse=1)
    # print(x, y ,z)
    r, theta, phi = cart2polar(x, y, z)
    longitude, latitude = polar2geo(r, theta, phi, x)
    # print(longitude, latitude)
    return longitude, latitude 

# canvas(title='STARLINK',
#      width=1200, height=1200,
#      center=vector(0,0,0), background=color.black)
# # distant_light(direction=vector(-1E10,1E10,-1E10), color=color.white)
# # distant_light(direction=vector(1E10,-0,1E10), color=color.white)
# lamp = local_light(pos=vector(-1E10,1E10,-1E10),color=color.white)
# lamp = local_light(pos=vector(1E10,-1E10,-0),color=color.white)

# earth = sphere(pos=vector(0,0,0), radius = 5, color=color.red)
# blob = sphere(pos=vector(100,0,0), radius = 5, color=color.blue)
# blob = sphere(pos=vector(100,0,0), radius = 5, color=color.blue)
# blob = sphere(pos=vector(0, 100,0), radius = 5, color=color.yellow)
# blob = sphere(pos=vector(0, 0, 100), radius = 5, color=color.green)
# x,y,z = polar2cart(100, (90/180)*math.pi, 90*math.pi/180)
# print(x,y,z)
# r,theta, phi = cart2polar(x,y,z)
# polar2geo(r, theta, phi)
# cart2geo(x,y,z)
# blob = sphere(pos=vector(x,y,z), radius = 5, color=color.white)
