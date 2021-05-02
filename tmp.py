from plotly.subplots import make_subplots
import plotly.graph_objects as go
from geometry import *

def chunks(lst,n):
    for i in range(0, len(lst), n):
            yield lst[i:i + n]


mapboxt = open(".mapbox_token").read().rstrip() #my mapbox_access_token 
fig = make_subplots(
    rows=2, cols=1,
    specs=[[{"type": "mapbox"}], [{"type": "mapbox"}]], vertical_spacing=0.01
)
for plot, j in zip([1,2],[0,5716]):
    longitudes, latitudes = fetch_locs(1, j)
    longitudes = list(chunks(longitudes, 22))
    latitudes = list(chunks(latitudes, 22))
    sizes = np.linspace(0,len(longitudes)/10,len(longitudes))

    for i in range(0,72): 
        fig.add_trace(go.Scattermapbox(
                lon=longitudes[i],
                lat=latitudes[i],
                mode='markers',
                marker=go.scattermapbox.Marker(size=sizes[i], color=colourdict[1][0]),   
                # text=['Montreal 1'],
            ), plot, 1)


        # fig.add_trace(go.Scattermapbox(
        #         lat=[45.6017],
        #         lon=[-73.7673],
        #         mode='markers',
        #         marker_size=14,
        #         text=['Montreal 2'],
        #     ), 2, 1)
# fig.update_layout(
#     autosize=True,
#     hovermode='closest')

#update the common attributes:
fig.update_mapboxes(
        bearing=0,
        accesstoken=mapboxt,
        # center=dict(
        #     lat=45,
        #     lon=-73
        # ),
        # pitch=0,
        )
   
#update different styles:
fig.update_layout(mapbox_style='light', mapbox2_style='light', width=1200, showlegend=False)
fig.show()
fig.write_image('figs/periodchange'+str(5717)+'.png')
