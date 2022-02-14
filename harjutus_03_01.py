#!/usr/bin/env python3

import math
import pandas as pd
import scipy.stats as st
from scipy.stats.distributions import chi2

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
# https://se.mathworks.com/help/stats/prob.normaldistribution.html
mean = st.t.interval(
    alpha=0.95, df=weight.size-1,
    loc=weight.mean(), scale=weight.sem()
)
# kaaluvahemik 95% usaldusnivoo korral
#  vahemikhinnang
# mu traditsiooniliselt tähistatakse keskväärtust
# need autod meie käsutuses valim
# weight.mean() punkthinnag
# mean[0] ja mean[1] usalduspiirid
print("      mu = %.2f [%.2f, %.2f]" %
      (weight.mean(), mean[0], mean[1])
      )
std = [481.243, 647.749]
print(weight.size)
std = st.t.interval(
    alpha=0.05, df=weight.size-1,
    loc=weight.std(), scale=weight.sem()
)


def CHISQINV(q, df):
    # https://stackoverflow.com/questions/53019080/chi2inv-in-python
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2.html
    return chi2.ppf(q, df)


N = weight.size
SD = weight.std()
alpha = 0.05

# https://www.graphpad.com/support/faq/the-confidence-interval-of-a-standard-deviation/
lowerLimit = SD*math.sqrt((N-1)/CHISQINV(1-(alpha/2), N-1))
upperLimit = SD*math.sqrt((N-1)/CHISQINV((alpha/2), N-1))

# sigma σ - statndardhälve
print("   sigma = %.3f [%.3f, %.3f]" %

      (weight.std(), lowerLimit, upperLimit)
      )

print('')
# https://se.mathworks.com/help/stats/prob.exponentialdistribution.html
# exponential distribution confidence interval
print('Expontial distribution:')
# this is not as example values 2340.26, 3549,9 from matlab fitdist(data, 'exp')
mean = st.expon.interval(
    alpha=0.95,
    loc=weight.mean(), scale=weight.sem()
)
# print(mean)

print('Normal distribution, trust level 99%:')
# vähendasime lubatud riski (95%->99%), suurendasime usaldusnivood
# usalduspiirkond läks suuremaks
mean = st.t.interval(
    alpha=0.99, df=weight.size-1,
    loc=weight.mean(), scale=weight.sem()
)
print("      %.2f, %.2f" %
      (mean[0], mean[1])
      )
alpha = 0.01

# https://www.graphpad.com/support/faq/the-confidence-interval-of-a-standard-deviation/
lowerLimit = SD*math.sqrt((N-1)/CHISQINV(1-(alpha/2), N-1))
upperLimit = SD*math.sqrt((N-1)/CHISQINV((alpha/2), N-1))

# sigma σ - statndardhälve
print("      %.3f, %.3f" %
      (lowerLimit, upperLimit)
      )
