from geometry import *
import pickle as pck
from copy import deepcopy
from pathlib import Path

colourdict = {1 : ['red', [255, 0, 0] ], 
                2 : ['green', [0, 255, 0]], 
                3: ['orange', [255, 165, 0]], 
                4: ['purple', [128, 0, 128]], 
                5: ['hotpink', [255, 105, 180]]}

# FeatureDict = pck.load(open('data/simFeatures.pck', 'rb'))
FeatureDict = {'Phase Features': {'Planes': [1], 
                                    'Sats per plane': [1], 
                                    'Inclination': [70], 
                                    'Altitude': [1150000], 
                                    'Offset': [0]}, 
                'Speed': 1000}
Phases = FeatureDict['Phase Features']
speed = FeatureDict['Speed']
earth_radius = 6.37E6

# calculates features for the phase depending on the altitude.
Phases['max comms range'] = [(np.sqrt((((earth_radius+10E3)+Phases['Altitude'][i])**2) - ((earth_radius+10E3)**2)))*2 for i in range(len(Phases['Altitude']))]
Phases['max ground reach'] = [Phases['Altitude'][i]*math.tan(rad(50))*3 for i in range(len(Phases['Altitude']))]

# Some popular locations defined by geographical coordinates
Locations = {'LDN': [-0.13, 51.5],
            'Johannesburg': [28.0, -26.2],
            'NYC': [-74.0, 40.7], 
            'SIN': [103.8, 1.4],
            'SFO': [-122.4, 37.8],
            }

phasenumPos = {}
for phasenum in range(1,2):
    # print('Reading positions file....')
    try:
        phasenumPos[str(phasenum)] = pck.load(open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/positions.pck', 'rb'))
    except:
        Path('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))).mkdir(parents=True, exist_ok=True)
        pck.dump([], open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/positions.pck', 'wb'))
        phasenumPos[str(phasenum)] = pck.load(open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/positions.pck', 'rb'))


def fetch_curr(phasenum):
    longitudes = []
    latitudes = []
    curr_positions = pck.load(open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/curr_positions.pck', 'rb'))
    for i in curr_positions[1]:
        lon, lat = cart2geo(i[0], i[1], i[2], curr_positions[0])
        longitudes.append(lon)
        latitudes.append(lat)
    return longitudes, latitudes, curr_positions[0]

def fetch_cart(phasenum, time):
    _, _, positions = fetch_curr(phasenum)
    return positions[str(time)]

def fetch_orbit():
    orbit = pck.load(open('data/'+str(int(Phases['Altitude'][phasenum-1]/1E3))+'/orbit.pck', 'rb'))
    longitudes, latitudes = [], []
    for t, v in orbit:
        lon, lat = cart2geo(v[0],v[1],v[2], t)
        longitudes.append(lon)
        latitudes.append(lat)
    return longitudes, latitudes

def calcGCR(source_loc, dest_loc):
    lon1, lat1 = source_loc
    lon2, lat2 = dest_loc
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371E3
    return c * r

# Satellite Acquisition. Finds the first closest satellite in range. 
def find_sat(phasenum, source, positions):
    temp_pos = deepcopy(positions)
    source_lon, source_lat = source
    lon_distances = [abs(source_lon - i[0]) for i in positions]
    lat_distances = [abs(source_lat - i[1]) for i in positions]

    temp_lons = deepcopy(lon_distances)
    temp_lats = deepcopy(lat_distances)
    while True:
        closest_lon = lon_distances.index(min(temp_lons))
        closest_lat = lat_distances.index(min(temp_lats))
        closest_lon_distance = calcGCR(source, positions[closest_lon])
        closest_lat_distance = calcGCR(source, positions[closest_lat])
        if closest_lon_distance <= closest_lat_distance:
            if closest_lon_distance < Phases['max ground reach'][phasenum-1]:
                return closest_lon, np.sqrt(closest_lon_distance**2 + Phases['Altitude'][phasenum-1]**2)
            else:
                temp_lons.pop(temp_lons.index(min(temp_lons)))
                temp_lats.pop(temp_lats.index(min(temp_lats)))
        else:
            if closest_lat_distance < Phases['max ground reach'][phasenum-1]:
                return closest_lat, np.sqrt(closest_lat_distance**2 + Phases['Altitude'][phasenum-1]**2)
            else:
                temp_lats.pop(temp_lats.index(min(temp_lats)))
                temp_lons.pop(temp_lons.index(min(temp_lons)))


# Finds all satellites in range which is much slower.
def findrange(phasenum, source, positions, fig=None):
    temp_pos = deepcopy(positions)
    source_lon, source_lat = source
    lon_distances = [abs(source_lon - i[0]) for i in positions]
    lat_distances = [abs(source_lat - i[1]) for i in positions]

    temp_lons = deepcopy(lon_distances)
    temp_lats = deepcopy(lat_distances)
    edges = []
    edge_distances = []
    for i in range(len(temp_lons)):
        closest_lon = lon_distances.index(min(temp_lons))
        closest_lat = lat_distances.index(min(temp_lats))
        closest_lon_distance = calcGCR(source, positions[closest_lon])
        closest_lat_distance = calcGCR(source, positions[closest_lat])

        if closest_lon_distance < Phases['max ground reach'][phasenum-1]:
            edges.append(closest_lon)
            edge_distances.append(closest_lon_distance)

        if closest_lat_distance < Phases['max ground reach'][phasenum-1]:
            edges.append(closest_lat)
            edge_distances.append(closest_lat_distance)

        temp_lats.pop(temp_lats.index(min(temp_lats)))
        temp_lons.pop(temp_lons.index(min(temp_lons)))
        
    closest_sat = edges[edge_distances.index(min(edge_distances))]

    return closest_sat, np.sqrt(min(edge_distances)**2 + Phases['Altitude'][phasenum-1]**2)

def calcDistanceBetween(source_loc, dest_loc):
    distance = np.sqrt((source_loc[0] - dest_loc[0])**2+(source_loc[1] - dest_loc[1])**2+(source_loc[2] - dest_loc[2])**2)
    return distance
