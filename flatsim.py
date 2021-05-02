import plotly.graph_objects as go
import numpy as np
import pickle as pck
# import geopandas as gpd
import base64
import pandas as pd
import plotly.io as plt_io
import vpython
from geometry import cart2geo, fetch_curr, colourdict, fetch_locs, fetch_orbit
import math
from plotly.subplots import make_subplots



# longitudes, latitudes = fetch_orbit()
# for i in range(len(longitudes)):
#     lon2.append(longitudes[i]+i/240)
#     lat2.append(latitudes[i] + i/240)
# print(lon2[0::100])
        # longitudes, latitudes, positions = fetch_curr(i)
def chunks(lst,n):
    for i in range(0, len(lst), n):
            yield lst[i:i + n]
fig = make_subplots(
    rows=2, cols=1,
    row_heights=[0.6, 0.6],
    specs=[[{"type": "scattergeo"}],
           [{"type": "scattergeo"}]],
    vertical_spacing=0.01)
for plot, j in zip([1,2],[0,5716]):
    # fig = go.Figure(
    #                 data=[go.Scattergeo(lon=[], lat=[],
    #                     name="frame",
    #                     mode="markers",
    #                     marker=dict(color='red', size=5))],
    #                 layout=go.Layout(
    #                     xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
    #                     yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
    #                     height = 700,
    #                     width = 1800,
    #                     margin=dict(l=5, r=80, t=100, b=80),
    #                     title ={
    #                     # 'text': "Starlink constellation in a geographical coordinate system",
    #                     'y':0.95,
    #                     'x':0.5,
    #                     'xanchor': 'center',
    #                     'yanchor': 'top'}
    #                     ))
    longitudes, latitudes = fetch_locs(1, j)
    longitudes = list(chunks(longitudes, 22))
    latitudes = list(chunks(latitudes, 22))
    print(longitudes[0])
    print(len(longitudes))
    sizes = np.linspace(0,len(longitudes)/10,len(longitudes))
    for i in range(0,72): 
        # print(len(sizes))
        # print(longitudes)
        size = 1*math.log(i+2,2)
        # print(size)
        fig.add_trace(go.Scattergeo(lon=longitudes[i], lat=latitudes[i],
                # name="frame",
                        mode="markers",
                        # text=np.arange(0,22,1),
                        marker=dict(color=colourdict[1][0], size=sizes[i])), row=plot, col = 1)

fig.show()
fig.update_layout(
    # template="plotly_dark",
    margin=dict(r=5, t=100, b=100, l=5),
    showlegend=False,
    height = 1200,
    width = 1800)
fig['layout']['annotations'][0].update(text='your text here')
fig.write_image('figs/periodchange'+str(5717)+'.pdf')

# for i in range(1,2):
        # longitudes, latitudes, positions = fetch_curr(i)
        # longitudes, latitudes = fetch_orbit()
        # sizes = np.linspace(0,len(longitudes)/100,len(longitudes))
        # print(len(sizes))
        # print(longitudes)
# fig.add_trace(go.Scattergeo(lon=longitudes, lat=latitudes,
#         name="frame",
#         mode="lines"))
# fig.add_trace(go.Scattergeo(lon=lon2, lat=latitudes,
#         name="frame",
#         mode="lines"))
                        # text=np.arange(0,22,1),
                        # marker=dict(color=colourdict[i][0], size=0)))