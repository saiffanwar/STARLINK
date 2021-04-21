import plotly.graph_objects as go
import numpy as np
import pickle as pck
# import geopandas as gpd
import base64
import pandas as pd
import plotly.io as plt_io
import vpython
from geometry import *

# def createdf(file):
#         with open(file, 'rb') as f:
#                 longitudes, latitudes, section, starting_positions  = pck.load(f)
#         all_cycles_lons = []
#         all_cycles_lats = []
#         for x in range(0, len(starting_positions)):
#             plane_cycle_lons = []
#             plane_cycle_lats = []
#             for init_pos in starting_positions[x]:
#                 index = longitudes[x].index(init_pos[0])
#                 sat_lons = longitudes[x][index:]+longitudes[x][:index]
#                 sat_lats = latitudes[x][index:]+latitudes[x][:index]
#                 plane_cycle_lons.append(sat_lons)
#                 plane_cycle_lats.append(sat_lats)
#             all_cycles_lons.append(plane_cycle_lons)
#             all_cycles_lats.append(plane_cycle_lats)
#         df = pd.DataFrame(
#                 {'OrbitalPath': zip(longitudes, latitudes),
#                 'Longitudes': all_cycles_lons,
#                 'Latitudes': all_cycles_lats
#                 }
#         )
#         return df


def init_plot(no_of_deployments):
        # df = pck.load('data/positions.pck')
        # df.head()
        with open('orbit.pck', 'rb') as f:
                orbit = pck.load(f)
        # for i in df['Planes']
        # longitudes = df['Longitudes']
        # latitudes = df['Latitudes']
        longitudes = []
        latitudes = []
        for i in orbit:
                lon, lat = cart2geo(i[0], i[1], i[2])
                longitudes.append(lon)
                latitudes.append(lat)

        t = np.linspace(-1, 1, 100)
        x = longitudes
        y = latitudes
        xm = -180
        xM = 180
        ym = -90
        yM = 90
        freq = 1
        # N = int(np.floor(len(x[0])/freq))+1
        # rang = np.arange(0, len(x[0][0]), freq)

        fig = go.Figure(
                data=[go.Scattergeo(lon=x, lat=y,
                # data=[go.Scattergeo(lon=[51.5074,1.3521], lat=[0.1278, 103.8198],
                     name="frame",
                     mode="lines",
                     line=dict(width=2, color="blue")),
    #       go.Scatter(x=x, y=y,
    #                  name="curve",
    #                  mode="lines",
    #                  line=dict(width=2, color="blue"))
                ],
                layout=go.Layout(
                xaxis=dict(range=[xm, xM], autorange=False, zeroline=False, title='Longitude'),
                yaxis=dict(range=[ym, yM], autorange=False, zeroline=False, title='Latitude'),
                # height = 800,
                # width = 1000,
                title ={
                'text': "Orbital Path of a single satellite as the Earth rotates",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
                        ))

        
        fig.show()
        
init_plot(1)