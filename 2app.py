import plotly.graph_objects as go
import numpy as np
import pickle as pck
import geopandas as gpd
import base64
import pandas as pd

def createdf():
        with open('planes1.pck', 'rb') as f:
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
        # print(np.shape(sat_longs))
        # print(np.shape(plane_cycle))
        print(np.shape(all_cycles_lons))
        # print(plane_cycle[30])
        # print(np.shape(starting_positions), starting_positions[0])
        df = pd.DataFrame(
                {'Longitudes': all_cycles_lons,
                'Latitudes': all_cycles_lats
                }
        )
        print(df.shape)
        return df

createdf()

df = createdf()
longitudes = df['Longitudes']
latitudes = df['Latitudes']
print(longitudes)
t = np.linspace(-1, 1, 100)
x = longitudes
y = latitudes
xm = -180
xM = 180
ym = -90
yM = 90
freq = 1
N = int(np.floor(len(x[0])/freq))+1
s = np.linspace(-1, 1, N)
# xx = lons
# yy = lats
rang = np.arange(0, len(x[0][0]), freq)
fig = go.Figure(
        data=[go.Scatter(x=x[0][0], y=y[0][0],
                     mode="lines",
                     line=dict(width=1, color="blue")),
                go.Scatter(x=x[0][0], y=y[0][0],
                     mode="lines",
                     line=dict(width=0.5, color="blue"))],

        layout=go.Layout(
        xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
        yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
        height = 600,
        width = 1200,
        title_text="Starlink Phase 1", hovermode="closest",
        updatemenus=[dict(type="buttons",
        buttons=[dict(label="Play",
        method="animate",
        args=[None, {"frame": {"duration": 100, "redraw": False},}])])]),

        frames=[go.Frame(
        data=[go.Scatter(
        x=[xi[k] for xi in x[0]]+
        [xi[k] for xi in x[1]]+
        [xi[k] for xi in x[2]]+
        [xi[k] for xi in x[3]]+
        [xi[k] for xi in x[4]]+
        [xi[k] for xi in x[5]]+
        [xi[k] for xi in x[6]]+
        [xi[k] for xi in x[7]]+
        [xi[k] for xi in x[8]]+
        [xi[k] for xi in x[9]]+
        [xi[k] for xi in x[10]]+
        [xi[k] for xi in x[11]]+
        [xi[k] for xi in x[12]]+
        [xi[k] for xi in x[13]]+
        [xi[k] for xi in x[14]]+
        [xi[k] for xi in x[15]]+
        [xi[k] for xi in x[16]]+
        [xi[k] for xi in x[17]]+
        [xi[k] for xi in x[18]]+
        [xi[k] for xi in x[19]]+
        [xi[k] for xi in x[20]]+
        [xi[k] for xi in x[21]]+
        [xi[k] for xi in x[22]]+
        [xi[k] for xi in x[23]]+
        [xi[k] for xi in x[24]]+
        [xi[k] for xi in x[25]]+
        [xi[k] for xi in x[26]]+
        [xi[k] for xi in x[27]]+
        [xi[k] for xi in x[28]]+
        [xi[k] for xi in x[29]]+
        [xi[k] for xi in x[30]]+
        [xi[k] for xi in x[31]],

        y=[yi[k] for yi in y[0]]+
        [yi[k] for yi in y[1]]+
        [yi[k] for yi in y[2]]+
        [yi[k] for yi in y[3]]+
        [yi[k] for yi in y[4]]+
        [yi[k] for yi in y[5]]+
        [yi[k] for yi in y[6]]+
        [yi[k] for yi in y[7]]+
        [yi[k] for yi in y[8]]+
        [yi[k] for yi in y[9]]+
        [yi[k] for yi in y[10]]+
        [yi[k] for yi in y[11]]+
        [yi[k] for yi in y[12]]+
        [yi[k] for yi in y[13]]+
        [yi[k] for yi in y[14]]+
        [yi[k] for yi in y[15]]+
        [yi[k] for yi in y[16]]+
        [yi[k] for yi in y[17]]+
        [yi[k] for yi in y[18]]+
        [yi[k] for yi in y[19]]+
        [yi[k] for yi in y[20]]+
        [yi[k] for yi in y[21]]+
        [yi[k] for yi in y[22]]+
        [yi[k] for yi in y[23]]+
        [yi[k] for yi in y[24]]+
        [yi[k] for yi in y[25]]+
        [yi[k] for yi in y[26]]+
        [yi[k] for yi in y[27]]+
        [yi[k] for yi in y[28]]+
        [yi[k] for yi in y[29]]+
        [yi[k] for yi in y[30]]+
        [yi[k] for yi in y[31]],
        mode="markers",
        marker=dict(color="red", size=5))])
                
                for k in rang]
                )
fig.add_layout_image(
        dict(
            source="https://cdn.substack.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2Fc10eea92-58db-4e3d-87d9-189f35bb7787_2058x1314.jpeg",
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
fig.update_layout(template="plotly_white")#, transition={'duration': 10})

fig.show()
