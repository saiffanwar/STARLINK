import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# import geopandas as gpd
# import shapely.geometry
import numpy as np
# import wget

fig = make_subplots(rows=1, cols=2,
                    column_widths=[0.35, 0.65],
                    specs=[[{"type": "scattergeo", "rowspan": 1}, {"type": "scattergeo", "rowspan": 1}]])

fig.add_trace(go.Scattergeo(lon=[0.1278, 103.8198], lat=[51.5074,1.3521], mode="lines",
                     line=dict(width=2, color="blue")), row=1,col=1)
fig.update_layout(geo = dict(
        # resolution = 50,
        # showland = True,
        # showlakes = True,
        # landcolor = 'rgb(204, 204, 204)',
        # countrycolor = 'rgb(204, 204, 204)',
        # lakecolor = 'rgb(255, 255, 255)',
        projection_type = "orthographic",
        # coastlinewidth = 2,
        # lataxis = dict(
        #     range = [20, 60],
        #     showgrid = True,
        #     dtick = 10
        ))
fig.add_trace(go.Scattergeo(lon=[0.1278, 103.8198], lat=[51.5074,1.3521], mode="lines",
                     line=dict(width=2, color="blue")), row=1,col=2)
fig.show()