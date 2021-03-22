import plotly.express as px
import geopandas as gpd
import pickle as pck
import numpy as np
import os
import plotly.graph_objects as go # or plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
if not os.path.exists("figs"):
    os.mkdir("figs")

shapefile = 'countrydata1/ne_10m_admin_0_countries.shp'
geo_df = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
colourdict = {1 : 'red', 2 : 'green', 3: 'orange', 4: 'purple', 5: 'teal'}

def plotly():

        fig = make_subplots(rows=1, cols=1)
        for i in range(1,2):
                with open('planes'+str(i)+'.pck', 'rb') as f:
                        longitudes, latitudes, section, starting_positions  = pck.load(f)

                for longs, lats in zip(longitudes, latitudes):
                        fig.add_trace( 
                        go.Scattergeo(lon= longs, lat= lats, 
                                        mode='lines',
                                        line=dict(width=1, color=colourdict[i]), 
                                        name='Section '+str(i)
                                        ))
                for plane_pos in starting_positions:
                        lons = [x[0] for x in plane_pos]
                        lats = [y[1] for y in plane_pos]
                        # fig.add_trace(
                        #         go.Frame(
                        #         data=[go.Scatter(
                        #         x=lons,
                        #         y=lats,
                        #         mode="markers",
                        #         marker=dict(color="red", size=10))])
                        # )
                        fig.add_trace(
                        go.Scattergeo(lon= lons, lat= lats, 
                                        marker=dict(color=colourdict[i], size=5), 
                                        ))
        
        # layout=go.Layout(
        # xaxis=dict(range=[-180, 180], autorange=False, zeroline=False),
        # yaxis=dict(range=[-90, 90], autorange=False, zeroline=False),
        # title_text="Kinematic Generation of a Planar Curve", hovermode="closest",
        # updatemenus=[dict(type="buttons",
        #                   buttons=[dict(label="Play",
        #                                 method="animate",
        #                                 args=[None])])]),
        # fig.write_image("figs/fig1.pdf")
        fig.show()
        

# plotly() 

def createdf():
        with open('planes1.pck', 'rb') as f:
                longitudes, latitudes, section, starting_positions  = pck.load(f)
        
        # print(np.shape(starting_positions), starting_positions[0])
        df = pd.DataFrame(
                {'Longitudes': np.array(latitudes).flatten(),
                'Latitudes': np.array(longitudes).flatten(),
                'Initial Positions': starting_positions
                }
        )
        print(df.head())
        return df
