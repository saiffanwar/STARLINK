from app import *
from sim_ops import *
import os

# init_sim()
#All LEO satellites

phase_sats1 = phase(32, 50, 53, 1150E3, 1)
# phase_sats2 = phase(32, 50, 53.8, 1100E3, 2)
# phase_sats3 = phase(8, 50, 74, 1130E3, 3)
# phase_sats4 = phase(5, 75, 81, 1275E3, 4)
# phase_sats5 = phase(6, 75, 70, 1325E3, 5)

# init_plot(1)

threading.Thread(target=orbit, args=(phase_sats1, 1150E3, 1)).start()
# threading.Thread(target=orbit, args=(phase_sats2, 1100E3, 2)).start()
# threading.Thread(target=orbit, args=(phase_sats3, 1130E3, 3)).start()
# threading.Thread(target=orbit, args=(phase_sats4, 1275E3, 4)).start()
# threading.Thread(target=orbit, args=(phase_sats5, 1325E3, 5)).start()

os.system('python app.py')
