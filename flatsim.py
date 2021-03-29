import plotly.graph_objects as go
import numpy as np
import pickle as pck
import geopandas as gpd
import base64
import pandas as pd
import plotly.io as plt_io

def createdf(file):
        with open(file, 'rb') as f:
                longitudes, latitudes, section, starting_positions  = pck.load(f)
        all_cycles_lons = []
        all_cycles_lats = []
        for x in range(0, len(starting_positions)):
            plane_cycle_lons = []
            plane_cycle_lats = []
            for init_pos in starting_positions[x]:
                index = longitudes[x].index(init_pos[0])
                sat_lons = longitudes[x][index:]+longitudes[x][:index]
                sat_lats = latitudes[x][index:]+latitudes[x][:index]
                plane_cycle_lons.append(sat_lons)
                plane_cycle_lats.append(sat_lats)
            all_cycles_lons.append(plane_cycle_lons)
            all_cycles_lats.append(plane_cycle_lats)
        df = pd.DataFrame(
                {'OrbitalPath': zip(longitudes, latitudes),
                'Longitudes': all_cycles_lons,
                'Latitudes': all_cycles_lats
                }
        )
        return df

colourdict = {1 : ['red', [255, 0, 0] ], 
                2 : ['green', [0, 255, 0]], 
                3: ['orange', [255, 165, 0]], 
                4: ['purple', [128, 0, 128]], 
                5: ['hotpink', [255, 105, 180]]}

def init_plot(no_of_deployments):
        df = createdf('data/planes1.pck')
        longitudes = df['Longitudes']
        latitudes = df['Latitudes']
        t = np.linspace(-1, 1, 100)
        x = longitudes
        y = latitudes
        xm = -180
        xM = 180
        ym = -90
        yM = 90
        freq = 1
        N = int(np.floor(len(x[0])/freq))+1

        rang = np.arange(0, len(x[0][0]), freq)
        fig = go.Figure(
                layout=go.Layout(
                xaxis=dict(range=[xm, xM], autorange=False, zeroline=False, title='Longitude'),
                yaxis=dict(range=[ym, yM], autorange=False, zeroline=False, title='Latitude'),
                height = 800,
                width = 1500,
                title ={
                'text': "Starlink constellation in a geographical coordinate system",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
                # title_text="Starlink Phase 1", hovermode="closest",
                updatemenus=[dict(type="buttons",
                buttons=[dict(label="Play",
                method="animate",
                args=[None, {"frame": {"duration": 100, "redraw": False},}])])]),
                frames=[go.Frame(
                data=[go.Scattergeo(
                lon=np.array([xi[k] for i in range(0,len(x)) for xi in x[i]]).flatten(),
                lat=np.array([yi[k] for i in range(0,len(x)) for yi in y[i]]).flatten(),
                mode="markers",
                marker=dict(color="red", size=5))])
                        
                        for k in rang]
                        )
        fig.add_trace( 
                        go.Scattergeo(lon= np.arange(-180,180.5,0.5), lat= np.zeros(360*2), 
                                        mode='lines',
                                        line=dict(width=1, color='blue'), 
                                        name='Equator'
                                        ))

        # fig.add_layout_image(
        #         dict(
        #         # source="https://cdn.substack.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fc10eea92-58db-4e3d-87d9-189f35bb7787_2058x1314.jpeg",
        #         xref="x",
        #         yref="y",
        #         x=-180,
        #         y=80,
        #         sizex=360,
        #         sizey=180,
        #         sizing="stretch",
        #         opacity=0.7,
        #         layer="below")
        # )
        # fig.update_layout(template="plotly_dark")#, transition={'duration': 10})
        # create our custom_dark theme from the plotly_dark template
        plt_io.templates["custom_dark"] = plt_io.templates["plotly_dark"]

        # set the paper_bgcolor and the plot_bgcolor to a new color
        plt_io.templates["custom_dark"]['layout']['paper_bgcolor'] = '#282c33'
        plt_io.templates["custom_dark"]['layout']['plot_bgcolor'] = '#282c33'

        # you may also want to change gridline colors if you are modifying background
        plt_io.templates['custom_dark']['layout']['yaxis']['gridcolor'] = '#ffffff'
        plt_io.templates['custom_dark']['layout']['xaxis']['gridcolor'] = '#ffffff'
        fig.layout.template = 'custom_dark'
        fig.update_geos(
        # resolution=100,
        # projection_type='natural earth',
        showcoastlines=True, coastlinecolor="White",
        showland=True, landcolor="#282c33",
        showocean=True, oceancolor="#282c33",
        # showlakes=True, lakecolor="Blue",
        # showrivers=True, rivercolor="Blue"
)
        for j in range(1,no_of_deployments+1):
                df = createdf('data/planes'+str(j)+'.pck')
                longitudes = df['Longitudes']
                latitudes = df['Latitudes']
                orbital_path = df['OrbitalPath']
                x = longitudes
                y = latitudes
                # fig.add_trace(go.Scattergeo(lon=np.array([x[i][0] for i in range(0,len(x))]).flatten(), 
                #                         lat=np.array([y[i][0] for i in range(0,len(x))]).flatten(),                        
                #                 mode="markers",
                #                 marker=dict(size=2, color=colourdict[j])))
                for longs, lats in orbital_path:
                        fig.add_trace( 
                        go.Scattergeo(lon= longs, lat= lats, 
                                        mode='lines',
                                        line=dict(width=1, color=colourdict[j][0]),
                                        showlegend=True if (orbital_path[0][0]==longs) is True else False, 
                                        name='Deployment Phase '+str(j)
                                        ))
                        fig.add_trace(
                                go.Scattergeo(
                                lon=np.array([xi[0] for i in range(0,len(x)) for xi in x[i]]).flatten(),
                                lat=np.array([yi[0] for i in range(0,len(x)) for yi in y[i]]).flatten(),
                                showlegend=False,
                                mode="markers",
                                marker=dict(color=colourdict[j][0], size=5)))
        
        fig.show()
        
# init_plot(5)