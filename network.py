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
from topology import manhattan as tp

def createNetworkGraph(phase, time):
    geopos = [[x.longitude, x.latitude] for x in phase.PhaseSats]
    cartpos = [[sat.pos.x, sat.pos.y, sat.pos.z] for sat in phase.PhaseSats]
    
    G, nodes = tp(phase)

    return G, nodes


def calcPath(phasenum, time, G, positions, nodes, mode='length'):

# uncomment for location based routes
    geoPos = [cart2geo(x[0], x[1], x[2]) for x in positions]
    source = Locations['LDN']
    destination = Locations['SIN']

    source_sat, source2ground = find_sat(phasenum, source, geoPos)
    dest_sat, dest2ground = find_sat(phasenum, destination, geoPos)        

    source = list(nodes.keys())[source_sat]
    destination = list(nodes.keys())[dest_sat]

    # source = 'a1'
    # destination = 'f8'
    # max_distance = Phases['max comms range'][phasenum-1]
    max_distance=None
    if mode == 'length':
        S = dict(nx.all_pairs_dijkstra_path(G, max_distance, 'weight')) # return all shortest paths
        D = dict(nx.all_pairs_dijkstra_path_length(G, max_distance, 'weight')) # return all shortest paths length (km)
    elif mode == 'hops':
        S = dict(nx.all_pairs_dijkstra_path(G, max_distance, None))
        D = dict(nx.all_pairs_dijkstra_path_length(G, max_distance, None)) # return all shortest paths length (hops)


    shortest_path = S[source][destination] # shortest path between a1 and j1
    distance = D[source][destination] # distance between a1 and j1 (km)

    #--- Shortest paths by number of hops
    return shortest_path, distance, G

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


def plot_3d_edges(nodes, G): 
        
    curves = []
    for i in G.edges:
        p1 = dict(pos=vector(nodes[i[0]][0], nodes[i[0]][1], nodes[i[0]][2]), color=color.green,  radius=10000)
        p2 = dict(pos=vector(nodes[i[1]][0], nodes[i[1]][1], nodes[i[1]][2]), color=color.green, radius=10000)
        distance = np.round(calcDistanceBetween([nodes[i[0]][0], nodes[i[0]][1], nodes[i[0]][2]], [nodes[i[1]][0], nodes[i[1]][1], nodes[i[1]][2]]),0)
        # print(distance, Phases['max comms range'][1-1])
        if distance < Phases['max comms range'][1-1]:
            curves.append(curve(p1,p2))
    
    return curves


def plotShortestPath(shortest_path, nodes, oldedges):
    edges = []
    [c.clear() for c in oldedges]

    for i in range(len(shortest_path)-1):
        sourcePos = nodes[shortest_path[i]]
        destPos = nodes[shortest_path[i+1]]

        edges.append(curve(sourcePos,destPos))

    return edges
