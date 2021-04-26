from network import *
import pickle as pck
from geometry import *
from pprint import pprint
import multiprocessing as mp
from tqdm import tqdm

section = 1
graphdict = {}
plane_positions = pck.load(open('data/positions'+str(int(Phases['Altitude'][section-1]/1E3))+'.pck', 'rb'))
# plane_positions = list(zip(np.arange(0,len(plane_positions),1), plane_positions)
# print(plane_positions['50'])
def graphFromPos(times):
    with open('data/graphdict'+str(int(Phases['Altitude'][section-1]/1E3))+'.pck', 'rb') as f:
        graphdict = pck.load(f)
    for i in times:
        if i%10 ==0:
            tic = time.time()
            G, positions = createNetworkGraph(i)
            graphdict[str(i)] = [G, positions]
            print(i,': ', time.time()-tic)
            print(graphdict.keys())
    while True:
        try:
            with open('data/graphdict'+str(int(Phases['Altitude'][section-1]/1E3))+'.pck', 'wb') as f:
                pck.dump(graphdict, f)
            return None
        except:
            pass
def chunks(lst,n):
    for i in range(0, len(lst), n):
            yield lst[i:i + n]

times = np.arange(1,len(plane_positions),1)
times = [int(i) for i in times[0:500]]
print(type(times[0]))
times = chunks(times,4)
if __name__ == '__main__':
    jobs = []
    for i in times:
        p = mp.Process(target=graphFromPos, args=(i,))
        jobs.append(p)
        p.start()
# print(graphdict.keys)
# graphFromPos(times)
# with open('data/graphdict'+str(int(Phases['Altitude'][section-1]/1E3))+'.pck', 'wb') as f:
#     pck.dump(graphdict, f)
# with open('graphdict1150.pck', 'rb') as f:
#     graphdict = pck.load(f)
# pprint(graphdict['10'])

# sat = find_sat([0.13, 51.5],graphdict['10'][1])
# print(sat)