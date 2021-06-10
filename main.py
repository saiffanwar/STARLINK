from pprint import pprint
import pickle as pck
import pandas as pd
import os

import click


def phase_setup():
    FeatureDict = pck.load(open('data/simFeatures.pck', 'rb'))

    Phases = FeatureDict['Phase Features']
    speed = FeatureDict['Speed'] 
    Phasedict = pd.DataFrame({'Phase Number': [1], 
                                'Altitude': Phases['Altitude'][0],
                                'Inclination': Phases['Inclination'][0],
                                'Planes': Phases['Planes'][0],
                                'Sats per plane': Phases['Sats per plane'][0],
                                'Offset': Phases['Offset'][0]})

    pprint(Phasedict)
    print('Simulation speed: ', str(speed)+'x')
    print('Would you like to change any of the features shown above? Select appropriate number.')
    print('(1) Constellation Characteristics')
    print('(2) Simulation speed')
    print('(3) Nothing, everything is correct')


    x = int(input(': '))

    if x == 1:
        # editphasenum = int(input('Which phase would you like to edit? (1-5): '))
        editphasenum = 1
        print('Leave the fields blank if you do not wish to change it.')
        new_val = input('Enter a new Altitude (m): ')
        if new_val:
            Phases['Altitude'][editphasenum-1] = int(new_val)
        new_val = input('Enter a new orbital inclination: (degrees): ')
        if new_val:
            Phases['Inclination'][editphasenum-1] = int(new_val)
        new_val = input('Enter a new number of planes: ')
        if new_val:
            Phases['Planes'][editphasenum-1] = int(new_val)
        new_val = input('Enter a new number of satellites per plane: ')
        if new_val:
            Phases['Sats per plane'][editphasenum-1] = int(new_val)
        new_val = input('Enter a new phase offset between planes: ')
        if new_val:
            Phases['Offset'][editphasenum-1] = int(new_val)

        Phasedict = pd.DataFrame({'Phase Number': [1,2,3,4,5], 
                                    'Altitude': Phases['Altitude'],
                                    'Inclination': Phases['Inclination'],
                                    'Planes': Phases['Planes'],
                                    'Sats per plane': Phases['Sats per plane'],
                                    'Offset': Phases['Offset']})
        print('These are the new constellation characteristics')
        pprint(Phasedict)
    elif x ==2:
        speed = int(input('What speed would you like to run the simulation at?'))

    FeatureDict = {'Phase Features': Phases,
                    'Speed': speed,
                    }
    pck.dump(FeatureDict, open('data/simFeatures.pck', 'wb'))




if __name__ == '__main__':
    phase_setup()
    # phasenums = input('How many phases would you like to deploy?')
    # print('Select mode:')
    # print('(1) Run full simulation')
    # print('(2) Compute graphs')
    # inp = int(input(': '))
    # if inp ==1:
    phasenums = 1
    time_limit = input('How long would you like to run the simulation for? (seconds): ')
    os.system('python3 startsim.py --phasenums '+str(phasenums)+' --time_limit '+str(time_limit))
    # elif inp==2:
    #     time_limit = input('Which time would you like to compute graphs up to? (seconds): ')
    #     os.system('python3 startsim.py --getGraphs ON --time_limit '+str(time_limit))
