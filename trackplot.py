import pickle as pck
from matplotlib import pyplot as plt
from geometry import *
import csv
from tkinter import *
from turtle import *
from vpython import *

canvas(title='STARLINK',
     width=1200, height=1200,
     center=vector(0,0,0), background=color.black)
# distant_light(direction=vector(-1E10,1E10,-1E10), color=color.white)
# distant_light(direction=vector(1E10,-0,1E10), color=color.white)
lamp = local_light(pos=vector(-1E10,1E10,-1E10),color=color.white)
lamp = local_light(pos=vector(1E10,-1E10,-0),color=color.white)


def plot_track(latitudes, longitudes):
    img = plt.imread('mercator.jpg')
    fig, ax = plt.subplots()
    ax.imshow(img, extent = [-180,180,-90,90])
    
    # for x, y in planes:
    ax.scatter(latitudes, longitudes, s=0.01, color='red')
    fig.tight_layout()
    fig.savefig('groundtrack.pdf')
    plt.show()

# latitudes = []
# longitudes = []
# with open('plane.csv','r') as file:
#         coords = csv.reader(file, delimiter=',')
#         len = 0
#         thetas = np.linspace(0, 2*math.pi, 19)
#         for row in coords:
#             # r, theta, phi = cart2polar
#             longitude = cart2geo(float(row[0]),float(row[1]), float(row[2]))[0]
#             latitude = cart2geo(float(row[0]),float(row[1]), float(row[2]))[1]
#             longitudes.append(longitude)
#             latitudes.append(latitude)

#             sphere(pos=vector(float(row[0]),float(row[1]), float(row[2])), radius = 250E2, color=color.white)
#             r, theta, phi = cart2polar(float(row[0]),float(row[1]), float(row[2]))
#             long, lat = polar2geo(r, theta, phi)
#             print('degs: ', r, theta*180/math.pi, phi*180/math.pi)
#             print(lat, long)
#             print(float(row[0]),float(row[1]), float(row[2]))
#             # print(phi)
#             x, y, z = polar2cart(r, theta, phi)
#             print(x, y, z)
#             print('-------------------------------')
#             sphere(pos=vector(x, y, z), radius = 260E2, color=color.red)
#             len += 1
# # # print(len)
# plt.scatter(latitudes, longitudes)
# plt.show()

