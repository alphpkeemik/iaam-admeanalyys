#!/usr/bin/env python3

import pandas as pd
import scipy.stats as st
df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


price = pd.to_numeric(df['price']).dropna()
df['weight'] = pd.to_numeric(df['weight'])
weight = df['weight'].dropna()

# standardhälve
print(weight.std())
# vahemikhinnang

print('Normal distribution:')

mean = st.t.interval(
    alpha=0.95, df=weight.size-1,
    loc=weight.mean(), scale=weight.sem()
)

print("      mu = %.2f [%.2f, %.2f]" %
      (weight.mean(), mean[0], mean[1])
      )
std = st.t.interval(
    alpha=0.95, df=weight.size-1,
    loc=weight.std(), scale=weight.sem()
)
print("   sigma = %.3f [%.3f, %.3f]" %

      (weight.std(), std[0], std[1])
      )

print('')
print('Expontial distribution:')
# this is not as example values 2340.26, 3549,9 from matlab fitdist(data, 'exp')
mean = st.expon.interval(
    alpha=0.95,
    loc=weight.mean(), scale=weight.sem()
)
# print(mean)
