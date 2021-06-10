from sim_utils import Phases, colourdict
import plotly.express as px
import plotly.graph_objects as go

def plotPathgeo(source_ground, destination_ground, phasenum, shortest_path, geopositions, fig=None):
    if not fig:
        fig = go.Figure(go.Scattermapbox( 
                        lon=[],lat=[],
                        ))
# for phasenum in range(1,2):
    no_of_planes = Phases['Planes'][phasenum-1]
    sats_per_plane = Phases['Sats per plane'][phasenum-1]
    colour = colourdict[phasenum][0]

    fig.add_trace(go.Scattermapbox(
            lon=[geopositions[shortest_path[0]][0], source_ground[0]],
            lat=[geopositions[shortest_path[0]][1], source_ground[1]],
            mode="lines",
            line=dict(width=2, color='green') 
            ))
    fig.add_trace(go.Scattermapbox(
            lon=[geopositions[shortest_path[-1]][0], destination_ground[0]],
            lat=[geopositions[shortest_path[-1]][1], destination_ground[1]],
            mode="lines",
            line=dict(width=2, color='green') 
            ))
    for i in range(len(shortest_path)-1):
        source = shortest_path[i]
        destination = shortest_path[i+1]
        fig.add_trace(go.Scattermapbox(
            lon=[geopositions[source][0], geopositions[destination][0]],
            lat=[geopositions[source][1], geopositions[destination][1]],
            mode="lines",
            line=dict(width=2, color=colourdict[phasenum][0]) 
            ))

    return fig
