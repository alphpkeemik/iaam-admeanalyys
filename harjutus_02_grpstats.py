import matplotlib.pyplot as plt
from numpy import NAN
import pandas as pd

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# - step 1 origin transform and histogram
map = {
    1: 'USA',
    2: 'EU',
    3: 'JAP',
}

df['origin'] = df['origin'].transform(lambda x: map[x] if x else NAN)
#df['weight'] = pd.to_numeric(df['weight'])
#df['price'] = pd.to_numeric(df['price'])
df['horsepower'] = pd.to_numeric(df['horsepower'])
df['displace'] = pd.to_numeric(df['displace'])

groupBy = df[['horsepower', 'origin', 'displace']].groupby(['origin'])
print(groupBy.size().reset_index(name='counts'))
print(groupBy.agg(['mean', 'count']))
print(groupBy.agg(['min', 'max', 'median']))

# conside also iqr implementation
# https://stackoverflow.com/a/40341529/9358736
