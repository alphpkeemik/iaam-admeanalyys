import matplotlib.pyplot as plt
import pandas as pd
import sys
histogram = True if sys.argv.__len__() > 1 else False

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

#plt.hist(df['origin'])
plt.hist(df['make'])
plt.xticks(rotation=90)


plt.show()
