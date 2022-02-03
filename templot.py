import matplotlib.pyplot as plt
import pandas as pd
import pickle as pck

with open('GeoPositions.pck', 'rb') as file:

    data = pck.load(file)
# df = pd.read_csv('GeoPositionss1.csv')

df = pd.DataFrame(data)
print(df.head())
xs, ys = [], []
for i in df['a1']:
    xs.append(i[0])
    ys.append(i[1])


plt.plot(xs, ys)

plt.show()