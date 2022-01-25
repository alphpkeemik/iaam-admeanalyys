from tkinter.ttk import Separator
import matplotlib.pyplot as plt
import pandas as pd

gallon = 3.8
mile = 1.609

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df['mpg'] = pd.to_numeric(df['mpg'])
df['weight'] = pd.to_numeric(df['weight'])


df = df.assign(fuel_consumption=lambda x: 1/x.mpg * gallon / mile * 100)
print(df)
df.plot("weight", "fuel_consumption", kind='scatter')

plt.show()
