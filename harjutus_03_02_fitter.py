#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from fitter import Fitter
from fitter import get_distributions


df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# https://www.kite.com/python/answers/how-to-fit-a-distribution-to-a-histogram-in-python
price = pd.to_numeric(df['price']).dropna()
weight = pd.to_numeric(df['weight']).dropna()
data = price
# print(get_distributions())
f = Fitter(data, bins=10, distributions=['norm', 'expon'])
f.fit()
f.summary()
