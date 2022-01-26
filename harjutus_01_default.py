import matplotlib.pyplot as plt
import pandas as pd

gallon = 3.8
mile = 1.609

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

df['mpg'] = pd.to_numeric(df['mpg'])
df['weight'] = pd.to_numeric(df['weight'])


df = df.assign(fuel_consumption=lambda x: 1/x.mpg * gallon / mile * 100)
#ax = df.plot.scatter("weight", "fuel_consumption", colorbar=True)
# this was actually not needed
# df.plot.line("weight", "fuel_consumption", ax=ax, color="#c4daff", linewidth=0.5)
carJapan = df[df['origin'] == 3]
carUsa = df[df['origin'] == 1]
# joined
# carUsa = df[(df['origin'] == 1)  | (df['origin'] == 2)]
carOther2 = df[df['origin'] == 2]

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(carJapan['weight'], carJapan['fuel_consumption'], s=10, c='b', marker="s", label='japan')
ax1.scatter(carUsa['weight'], carUsa['fuel_consumption'], s=10, c='r', marker="1", label='usa')
ax1.scatter(carOther2['weight'], carOther2['fuel_consumption'], s=10, c='y', marker="2", label='others 2')
#plt.scatter(df['weight'], carJapan['fuel_consumption'], carOther['fuel_consumption'])
plt.legend(loc='upper left');

plt.show()
