import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import pickle as pck
import numpy as np
import matplotlib.pyplot as plt
from path_utils import plotPathgeo
from sim_utils import find_sat, fetch_locs, fetch_curr, fetch_cart, calcDistanceBetween, Phases, colourdict, Locations, findrange
import time as tm
from copy import deepcopy
import string
from tkinter import *
from turtle import *
from vpython import *
import math
from geometry import rad, deg, cart2geo, cart2polar, polar2cart
import time

# IMPORT RELEVANT TOPOLOGY HERE:
from topology import double_graph

def createNetworkGraph(phasenum, time, positions):
    longitudes, latitudes = fetch_locs(phasenum, time)
    # positions = fetch_cart(phasenum, time)
    geopositions = list(zip(longitudes, latitudes))

    m = Phases['Planes'][phasenum-1]
    n = Phases['Sats per plane'][phasenum-1]
    
    G, nodes = double_graph(m,n, positions)

    return G, nodes

def calcPathold(phasenum, source, destination, time, graphdict=None):

    [G, positions] = pck.load(open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/'+str(time)+'.pck', 'rb'))

    tic = tm.time()
    source_sat, source2ground = find_sat(phasenum, source, positions)
    source_calc_time1 = tm.time() - tic
    tic = tm.time()
    dest_sat, dest2ground = find_sat(phasenum, destination, positions)        
    dest_calc_time1 = tm.time() - tic


    shortest_path = list(nx.single_source_dijkstra(G, source_sat, dest_sat,weight='weight'))
    path = shortest_path[1]
    rtt = shortest_path[0] + source2ground + dest2ground

    return rtt, path, positions

# def calcPath(phasenum, source, destination, time):

# This function is used to create a static path image.
def onePlot(loc1, loc2, time):
    mapbox_access_token = open(".mapbox_token").read()
    fig = go.Figure(
                data=[go.Scattermapbox(lon=[], lat=[],
                    name="frame",
                    mode="markers",
                    marker=go.scattermapbox.Marker(size=5, color='red'))],
                layout=go.Layout(
                    xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
                    yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
                    height = 800,
                    width = 1400
                    ))

    for phasenum in range(1,2):
        longitudes, latitudes = fetch_locs(phasenum, time)
        fig.add_trace(go.Scattermapbox(lon=longitudes, lat=latitudes,
                        name="frame",
                        mode="markers",
                        text = np.arange(0,Phases['Planes'][phasenum-1]*Phases['Sats per plane'][phasenum-1],1),
                        marker=go.scattermapbox.Marker(size=5, color=colourdict[phasenum][0])))

        source = Locations[loc1]
        destination = Locations[loc2]


        fig.add_trace(go.Scattermapbox(lon=[source[0], destination[0]], lat=[source[1], destination[1]],
                        name="frame",
                        mode="markers",
                        marker=go.scattermapbox.Marker(size=10, color='green')))
        rtt, path, positions = calcPath(phasenum, source, destination, time)

        fig.add_annotation(
            text="Time Elapsed: "+str(time)+"s, Round Trip Time: "+str(2*np.round(rtt/300E3,3))+"ms",
            showarrow=False,
            yshift=-185, font=dict(size=18))
        fig.add_annotation(
            text="Path: "+str([str(i) for i in path])+', Hop count: '+str(2*(len(path)+2)),
            showarrow=False,
            yshift=-205, font=dict(size=18))
        fig = plotPathgeo(source, destination, phasenum, path, positions, fig)
        fig.update_layout(showlegend=False,  
        mapbox=dict(
            accesstoken=mapbox_access_token, 
            style='light', zoom=0.7))
    # fig.write_image('figs/exp2/'+str(loc1)+str(loc2)+'longest.pdf')
    fig.show()

def plotEdges(G, time=0):
    mapbox_access_token = open(".mapbox_token").read()
    fig = go.Figure(
                data=[go.Scattergeo(lon=[], lat=[],
                    name="frame",
                    mode="markers",
                    marker=dict(size=5, color='red'))],
                layout=go.Layout(
                    xaxis=dict(range=[-180, 180], autorange=False, zeroline=False, title='Longitude'),
                    yaxis=dict(range=[-90, 90], autorange=False, zeroline=False, title='Latitude'),
                    height = 800,
                    width = 1400
                    ))
    for phasenum in range(1,2):
        longitudes, latitudes = fetch_locs(phasenum, time)
        fig.add_trace(go.Scattergeo(lon=longitudes, lat=latitudes,
                        name="frame",
                        mode="markers",
                        text = np.arange(0,Phases['Planes'][phasenum-1]*Phases['Sats per plane'][phasenum-1],1),
                        marker=dict(size=5, color=colourdict[phasenum][0])))


    m = Phases['Planes'][phasenum-1]
    n = Phases['Sats per plane'][phasenum-1]
    letters = string.ascii_letters

    level = letters[0:m]
    pos = 0
    nodes = {}
    for l in level:
        for i in range(1, n + 1):
            nodes[l+str(i)] = [longitudes[pos], latitudes[pos]]

        
            pos +=1
    # print(nodes)
    print(nodes)
    for i in G.edges:
        # print(nodes[i[0]], nodes[i[1]])
        fig.add_trace(go.Scattergeo(
        mode = "markers+lines",
        lon = [nodes[i[0]][0], nodes[i[1]][0]],
        lat = [nodes[i[0]][1], nodes[i[1]][1]],
        marker=dict(size=5, color=colourdict[phasenum][0])))

    # fig.update_layout(showlegend=True,  
    #     mapbox=dict(
    #         accesstoken=mapbox_access_token, 
    #         style='light', zoom=0.7))
    fig.show()


def plot_3d_edges(nodes, G, phasenum): 
        
    curves = []

    for i in G.edges:
        p1 = dict(pos=vector(nodes[i[0]][0], nodes[i[0]][1], nodes[i[0]][2]), color=color.green,  radius=10000)
        p2 = dict(pos=vector(nodes[i[1]][0], nodes[i[1]][1], nodes[i[1]][2]), color=color.green, radius=10000)
        distance = np.round(calcDistanceBetween([nodes[i[0]][0], nodes[i[0]][1], nodes[i[0]][2]], [nodes[i[1]][0], nodes[i[1]][1], nodes[i[1]][2]]),0)
        # print(distance, Phases['max comms range'][1-1])
        if distance < Phases['max comms range'][1-1]:
            curves.append(curve(p1,p2))
    
    # time.sleep(1)
    return curves
    


# The code below can be used to observe the Network graph at a specific timepoint. They are humanly incomprehensible.
# [G, positions] = createNetworkGraph(1,0)
# cart_pos = fetch_cart(1, 0)

# plot_3d_edges(cart_pos, G, 1)

# [G, positions] = pck.load(open('data/'+str(int(Phases['Altitude'][1-1]/1E3))+'/'+str(10)+'.pck', 'rb'))

# pos = nx.circular_layout(G)
# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
# nx.draw_networkx_edges(G,pos)
# nx.draw(G, with_labels = True)
# onePlot('NYC', 'LDN',10)
# plotEdges(G)
# plt.show()