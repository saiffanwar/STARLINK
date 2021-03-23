import plotly.graph_objects as go
import numpy as np
import pickle as pck
import geopandas as gpd
import base64
import pandas as pd

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

colourdict = {1 : 'red', 2 : 'green', 3: 'orange', 4: 'purple', 5: 'teal'}

def init_plot():
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
                xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
                yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
                height = 1200,
                width = 2400,
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

        fig.add_layout_image(
                dict(
                # source="https://cdn.substack.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fc10eea92-58db-4e3d-87d9-189f35bb7787_2058x1314.jpeg",
                xref="x",
                yref="y",
                x=-180,
                y=80,
                sizex=360,
                sizey=180,
                sizing="stretch",
                opacity=0.7,
                layer="below")
        )
        # fig.update_layout(template="plotly_white")#, transition={'duration': 10})

        for j in range(1,6):
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
                                        line=dict(width=1, color=colourdict[j]), 
                                        name='Section '+str(j)
                                        ))
                        fig.add_trace(
                                go.Scattergeo(
                                lon=np.array([xi[0] for i in range(0,len(x)) for xi in x[i]]).flatten(),

                                lat=np.array([yi[0] for i in range(0,len(x)) for yi in y[i]]).flatten(),
                                mode="markers",
                                marker=dict(color=colourdict[j], size=5)))
        
        fig.show()
        
init_plot()