import math
import numpy as np
from tkinter import *
from turtle import *
from vpython import *

def rad(x):
    return (x*math.pi/180)

def deg(x):
    return (x*180/math.pi)
    
# VPython's coordinate axis are wrong according to standard practice.
# This function rearranges the coordinates to comply with the library.
def std2vpy(old_x,old_y,old_z, inverse=0):
    new_x = old_y
    new_y = old_z
    new_z = old_x
    if (inverse == 1):
        new_x = old_z
        new_y = old_x
        new_z = old_y 
    return new_x, new_y, new_z

def polar2cart(r, theta, phi): 
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)

    x,y,z = std2vpy(x,y,z)
    # if (phi > math.pi/2):
    #     x = -x
    #     z = -z
    return [x, y, z]
    
def polar2geo(r, theta, phi, x,y,z):
    latitude = (math.pi/2 - phi)
    
    if theta < 0:
        theta = math.pi + theta
    if x > 0:
        theta = -math.pi + theta
    longitude = theta

        
    # print(deg(latitude), deg(longitude))
    return deg(longitude), deg(latitude)
    
def cart2polar(x, y, z):
    x,y,z = std2vpy(x,y,z,inverse=1)
    r = np.sqrt((x**2)+(y**2)+(z**2))
    # print(z/r)
    phi = np.arccos(z/r)


    theta = np.arctan(y/x)
    return r, theta, phi


def cart2geo(x, y, z):
    # print(x,y,z)
    r, theta, phi = cart2polar(x, y, z)
    longitude, latitude = polar2geo(r, theta, phi,x,y,z)
    return longitude, latitude
