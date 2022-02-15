#!/usr/bin/env python3

import numpy
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)


df['price'] = pd.to_numeric(df['price'])
df['weight'] = pd.to_numeric(df['weight'])
df['mpg'] = pd.to_numeric(df['mpg'])
df = df.dropna()


X = numpy.array(df['weight']).reshape(-1, 1)
Y = numpy.array(df['mpg']).reshape(-1, 1)
plt.scatter(X, Y)

reg = LinearRegression().fit(X, Y)
print('score %f' % (reg.score(X, Y)))
plt.plot(X, reg.predict(X), 'r', linewidth=0.5)

# https://www.geeksforgeeks.org/solving-linear-regression-in-python/
# Slope = 28/10 = 2.8
# Intercept = 14.6 – 2.8 * 3 = 6.2
# Therefore,
# The desired equation of the regression model is y = 2.8 x + 6.2
print('y = %f x + %f' % (reg.coef_[0][0], reg.intercept_[0]))
