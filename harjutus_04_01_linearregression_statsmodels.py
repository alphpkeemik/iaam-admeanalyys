#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
import statsmodels.api as sm


df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


df['price'] = pd.to_numeric(df['price'])
df['weight'] = pd.to_numeric(df['weight'])
df['mpg'] = pd.to_numeric(df['mpg'])
df = df.dropna()

# https://www.statology.org/residual-plot-python/
model = ols('mpg ~ weight', data=df).fit()
fig = plt.figure(figsize=(12, 8))
# fig is https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.RegressionResults.html#statsmodels.regression.linear_model.RegressionResults
fig = sm.graphics.plot_regress_exog(model, 'weight', fig=fig)
