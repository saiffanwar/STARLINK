# from geometry import Locations, Phases, fetch_curr, calcDistanceBetween
from turtle import width
import pickle as pck
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.dates import date2num

import pickle as pck
from sim_utils import Phases, Locations, calcGCR
from tqdm import tqdm
import datetime


plt.style.use('classic')
plt.rc('font',**{'family':'serif','serif':['Times']})
# plt.rc('text', usetex=True)


def plotRTT():
    with open('data/1150/pathLengths.pck', 'rb') as f:
        pathLengths = pck.load(f)
    ts, ys = [], []
    rtts, gcrs = [], []
    for i in pathLengths:
        ts.append(i[0])
        distance = i[1][0]
        gcr = i[1][1]
        print(distance, gcr)
        rtt = distance/300E6
        rtts.append(distance)
        gcrtime = gcr/204.081E6 
        gcrs.append(gcr)
        normalisedRTT = rtt/gcrtime
        print(distance, gcr, normalisedRTT)
        ys.append(normalisedRTT)
        # 204.081E6 is the speed of light through optical fibre with refractive index 1.47

    USABLE_WIDTH_mm = 200
    USABLE_HEIGHT_mm = 300
    YANK_RATIO = 0.0393701
    USABLE_WIDTH_YANK = USABLE_WIDTH_mm*YANK_RATIO
    USABLE_HEIGHT_YANK = USABLE_HEIGHT_mm*YANK_RATIO
    SUBPLOT_FONT_SIZE = 12

    fig, ax = plt.subplots(nrows=2, ncols=1, sharex='col', figsize=(USABLE_WIDTH_YANK, USABLE_HEIGHT_YANK), tight_layout=True)
    ax[0].plot(ts, ys, linewidth=2, color='red')
    ax[0].set_ylim(-2,2)
    ax[0].set_xlim(0, ts[-1]+1)

    ax[1].plot(ts,rtts, linewidth=2)

    ax[1].plot(ts, gcrs, linewidth=2)
    ax[1].legend(['RTT using Satellites', 'RTT using GCR optical fibre'], loc='center', bbox_to_anchor=(0.5, 1.05), ncol=2)

    ax[0].set_title('RTT between source and destination normalised with \n GCR RTT using terrestrial optical fibre\n')
    ax[1].set_title('Comparing RTT throughout time\n \n')
    for i in [0,1]:
        ax[i].grid()
    plt.show()

plotRTT()