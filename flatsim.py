import plotly.graph_objects as go
import numpy as np
import pickle as pck
# import geopandas as gpd
import base64
import pandas as pd
import plotly.io as plt_io
import vpython
from geometry import *



fig = go.Figure(
                data=[go.Scattergeo(lon=[], lat=[],
                    name="frame",
                    mode="markers",
                    marker=dict(color='red', size=5))],
                layout=go.Layout(
                    xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
                    yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
                    height = 700,
                    width = 1500,
                    title ={
                    'text': "Starlink constellation in a geographical coordinate system",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'}
                    ))
# for i in range(1,2):
#         longitudes, latitudes = fetch_curr(i)
#         print(longitudes)
#         fig.add_trace(go.Scattergeo(lon=longitudes, lat=latitudes,
#                 name="frame",
#                         mode="markers",
#                         marker=dict(color=colourdict[i][0], size=5)))

fig.show()