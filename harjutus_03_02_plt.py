#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import scipy
import matplotlib.pyplot as plt

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# https://www.kite.com/python/answers/how-to-fit-a-distribution-to-a-histogram-in-python
price = pd.to_numeric(df['price']).dropna()
weight = pd.to_numeric(df['weight']).dropna()
data = price
_, bins, _ = plt.hist(data, 10, density=1, alpha=0.5)

mu, sigma = scipy.stats.norm.fit(data)
best_fit_line = scipy.stats.norm.pdf(bins, mu, sigma)
plt.plot(bins, best_fit_line)
plt.grid(True)
plt.xlabel('Prices')
plt.ylabel('Probability')
plt.title(
    r'$\mathrm{Histogram\ of\ IQ:}\ \mu=%.3f,\ \sigma=%.3f$' % (mu, sigma))
