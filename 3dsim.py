from app import *
from sim_ops import *
import os

#All LEO satellites

phase_sats1 = phase(72, 22, 53, 550E3, 1)
phase_sats2 = phase(72, 22, 53.2, 540E3, 2)
# phase_sats3 = phase(36, 20, 70, 570E3, 3)
# phase_sats4 = phase(6, 58, 97.6, 560E3, 4)
# phase_sats5 = phase(4, 43, 97.6, 560E3, 5)

os.system('python app.py')
