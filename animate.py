import plotly.graph_objects as go

import numpy as np
from flatsim import *



# Generate curve data
t = np.linspace(-1, 1, 100)
x = t + t ** 2
y = t - t ** 2
xm = np.min(x) - 1.5
xM = np.max(x) + 1.5
ym = np.min(y) - 1.5
yM = np.max(y) + 1.5
N = 50
s = np.linspace(-1, 1, N)
xx = s + s ** 2
yy = s - s ** 2
vx = 1 + 2 * s
vy = 1 - 2 * s  # v=(vx, vy) is the velocity
speed = np.sqrt(vx ** 2 + vy ** 2)
ux = vx / speed  # (ux, uy) unit tangent vector, (-uy, ux) unit normal vector
uy = vy / speed

xend = xx + ux  # end coordinates for the unit tangent vector at (xx, yy)
yend = yy + uy

xnoe = xx - uy  # end coordinates for the unit normal vector at (xx,yy)
ynoe = yy + ux

df = createdf('data/planes1.pck')
longitudes = df['Longitudes']
latitudes = df['Latitudes']
t = np.linspace(-1, 1, 100)
lon = longitudes
lat = latitudes
xm = -180
xM = 180
ym = -90
yM = 90
freq = 1
# N = int(np.floor(len(x[0])/freq))+1

rang = np.arange(0, len(lon[0][0]), freq)
# print(rang)
lon = np.array([xi[k] for i in range(0,len(lon)) for xi in lon[i] for k in rang]).flatten()
lat = np.array([yi[k] for i in range(0,len(lat)) for yi in lat[i] for k in rang]).flatten()

print(-lat)


# print([xx[k] for k in range(N)])
# Create figure
fig = go.Figure(
    data=[go.Scatter(x=[], y=[],
                     name="frame",
                     mode="lines",
                     line=dict(width=2, color="blue")),
    #       go.Scatter(x=x, y=y,
    #                  name="curve",
    #                  mode="lines",
    #                  line=dict(width=2, color="blue"))
          ],
    layout=go.Layout(width=600, height=600,
                     xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
                     yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
                     title="Moving Frenet Frame Along a Planar Curve",
                     hovermode="closest",
                     updatemenus=[dict(type="buttons",
                                       buttons=[dict(label="Play",
                                                     method="animate",
                                                     args=[None])])]),

    frames=[go.Frame(
        data=[go.Scatter(
            x=[lon[i], lon[i]],
            y=[lat[i], -lat[i]],
            mode="markers",
            marker=dict(color='red', size=5))
        ]) for i in range(len(lon))]
)

fig.show()