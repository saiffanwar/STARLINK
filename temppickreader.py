import pickle as pck


with open('data/simFeatures.pck', 'rb') as file:
            print(pck.load(file))
file.close()

