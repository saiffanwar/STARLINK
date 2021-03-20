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

# shapefile = 'countrydata/ne_110m_admin_0_countries.shp'
# geo_df = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
colourdict = {1 : 'red', 2 : 'green', 3: 'orange', 4: 'purple', 5: 'teal'}

def plotly():
        fig = make_subplots(rows=1, cols=1)

        for i in range(1,6):
                with open('planes'+str(i)+'.pck', 'rb') as f:
                        longitudes, latitudes, section, starting_positions  = pck.load(f)
                latitudes = np.array(latitudes).flatten()
                longitudes = np.array(longitudes).flatten()
                init_longs = []
                init_lats = []
                for x in starting_positions:
                        for j in x:
                                # print(j)
                                init_longs.append(j[0])
                                init_lats.append(j[1])
                fig.add_trace(
                go.Scattergeo(lon= longitudes, lat= latitudes, 
                                marker=dict(color=colourdict[i], size=2), 
                                name='Section '+str(i)
                                ))
                fig.add_trace(
                go.Scattergeo(lon= np.array(init_longs).flatten(), lat= np.array(init_lats).flatten(), 
                                marker=dict(color=colourdict[i], size=5), 
                                name='Section '+str(i)
                                ))
                print(np.array(init_longs).flatten())
        # fig.write_image("figs/fig1.pdf")
        fig.show()


        # latitudes = np.array(latitudes).flatten()
        # longitudes = np.array(longitudes).flatten()

        # latitudes = latitudes[100:150]
        # longitudes = longitudes[100:150]
        # print(np.sort(latitudes), np.sort(longitudes))

        # for i in range(0, len(latitudes)):
        #         print(latitudes[i], longitudes[i])
        # px.set_mapbox_access_token(open(".mapbox_token").read())
        # fig = go.Figure()
        # df = createdf()
        # latitudes = df['Latitudes']
        # longitudes = df['Longitudes']
        

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




# createdf()
plotly()