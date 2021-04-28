import math
import numpy as np
from tkinter import *
from turtle import *
from vpython import *
import pickle as pck
import pandas as pd
from copy import deepcopy 
import sys

def rad(x):
    return (x*math.pi/180)

def deg(x):
    return (x*180/math.pi)

colourdict = {1 : ['red', [255, 0, 0] ], 
                2 : ['green', [0, 255, 0]], 
                3: ['orange', [255, 165, 0]], 
                4: ['purple', [128, 0, 128]], 
                5: ['hotpink', [255, 105, 180]]}

# Phases = {'Planes': [72, 72, 36, 6, 4] , 
#             'Sats per plane': [22, 22, 20, 58, 43] , 
#             'Inclination': [53, 53.2, 70, 97.6, 97.6], 
#             'Altitude': [550E3, 540E3, 570E3, 560E3, 560E3]}
earth_radius = 6.37E6

Phases = {'Planes': [72, 6],
            'Sats per plane': [22, 20],
            'Inclination': [53,76],
            'Altitude': [1150E3, 570E3],
            'Offset': [49, 5]}

# calculates features for the phase depending on the altitude.
Phases['max comms range'] = [np.sqrt(((earth_radius+Phases['Altitude'][0])**2) - (earth_radius**2)), 
                            np.sqrt(((earth_radius+Phases['Altitude'][1])**2) - (earth_radius**2))]
Phases['max ground reach'] = [Phases['Altitude'][0]*math.tan(rad(40)),
                            Phases['Altitude'][1]*math.tan(rad(40))]

# Some popular locations defined by geographical coordinates
Locations = {'London': [-0.13, 51.5],
            'Johannesburg': [28.0, -26.2],
            'New York': [-74.0, 40.7], 
            'Singapore': [103.8, 1.35]}

try:    
    print('Reading positions file....')
    positions = pck.load(open('data/positions'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'rb'))
    print('File opened.')
except:
    pck.dump([], open('data/positions'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'wb'))

# try:
#     print('Reading graphdict file....')
#     graphdict = pck.load(open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'rb'))
#     print('File opened.')
# except:
#     pck.dump([], open('data/graphdict'+str(int(Phases['Altitude'][1-1]/1E3))+'.pck', 'wb'))

speed = 10
    


def sign(x):
    if x < 0:
        return 'negative'
    elif x > 0:
        return 'positive'
    else:
        return 'zero'
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
    

def geo2polar(longitude, latitude):
    phi = math.pi/2 - latitude
    if longitude >= 0:
        theta = rad(longitude)
    if longitude < 0:
        theta = math.pi - rad(longitude)
    
    r = 550E3
    return r, theta, phi


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
    return np.round(longitude,2), np.round(latitude,2)

def fetch_locs(deployment,t):
    df = pd.DataFrame({
        'Plane': []
    })
    longitudes = []
    latitudes = []
    # no_of_planes = plane_positions[0][0]
    # sats_per_plane = plane_positions[0][1]
    # print(len(positions[str(t)]))
    for i in positions[str(t)]:
        lon, lat = cart2geo(i[0], i[1], i[2])
        longitudes.append(lon)
        latitudes.append(lat)
    return longitudes, latitudes

def fetch_curr(section):
    df = pd.DataFrame({
        'Plane': []
    })
    longitudes = []
    latitudes = []
    plane_positions = pck.load(open('data/plane_positions'+str(int(Phases['Altitude'][section-1]/1E3))+'.pck', 'rb'))
    # no_of_planes = plane_positions[0][0]
    # sats_per_plane = plane_positions[0][1]
    for i in plane_positions[1]:
        lon, lat = cart2geo(i[0], i[1], i[2])
        longitudes.append(lon)
        latitudes.append(lat)
    return longitudes, latitudes, plane_positions[0]

# This function takes the current position of a satellite and adjusts it to match the earths rotation.
def rotate_orbit(theta, x):
    old_theta = theta
    if x>=0:
        if theta >= 0:
            theta = deg(theta)
        else:
            theta = 180 + deg(theta)
    if x<0:
        if theta >= 0:
            theta = 180 + deg(theta)
        else:
            theta = 360 + deg(theta)

    return rad(theta-1/240)


def fetch_orbit():
    orbital_path = pck.load(open('data/orbit.pck', 'rb'))
    longitudes = [x[0] for x in orbital_path]
    latitudes = [x[1] for x in orbital_path]
    return longitudes, latitudes

def calcDistanceBetween(source_loc, dest_loc):
    distance = np.sqrt((((source_loc[0] - dest_loc[0])*111.32E3)**2)+(((source_loc[1] - dest_loc[1])*111E3)**2))
    return distance

def find_sat(source, positions):
    section=1
    temp_pos = deepcopy(positions)
    source_lon, source_lat = source
    lon_distances = [abs(source_lon - i[0]) for i in positions]
    lat_distances = [abs(source_lat - i[1]) for i in positions]

    temp_lons = deepcopy(lon_distances)
    temp_lats = deepcopy(lat_distances)
    try:
        while True:
            closest_lon = lon_distances.index(min(temp_lons))
            closest_lat = lat_distances.index(min(temp_lats))
            # print(closest_lon, closest_lat, positions[closest_lon], positions[closest_lat])

            if calcDistanceBetween(source, positions[closest_lon]) < Phases['max ground reach'][section-1]:
                # print('Sat Found!')
                return closest_lon
            else:
                temp_lons.pop(temp_lons.index(min(temp_lons)))
            if calcDistanceBetween(source, positions[closest_lat]) < Phases['max ground reach'][section-1]:
                # print('Sat Found!')
                return closest_lat
            else:
                temp_lats.pop(temp_lats.index(min(temp_lats)))
    except ValueError:
        print('The requested ground position does not have a satellite close enough to communicate!')
        sys.exit(1)