#!/usr/bin/env python3

import pandas as pd
from statsmodels.stats.diagnostic import lilliefors
import numpy as np
import scipy

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

price = pd.to_numeric(df['price']).dropna()
weight = pd.to_numeric(df['weight']).dropna()


# https://se.mathworks.com/help/stats/lillietest.html
# https://www.statsmodels.org/dev/generated/statsmodels.stats.diagnostic.lilliefors.html
print(' --- hind ---')
r = lilliefors(price)
print("""hind lilliefors norm:
      h = NA normaaljaotus (hüpotees 0) või mitte  (1), mathlab 1
      p = %f väiksed p väärtused hüpoteesi 1 poolt
      k = %.5f
      c = NA kui c on suurem kui k, siis on hüpotees 0, h väärtus k ja c vahekorrast 
      """ %
      (r[1], r[0])
      )
      
# there is no Alpha parameter for python 

r = lilliefors(price, dist='exp')
print("""hind lilliefors exp:
      h = NA normaaljaotus (hüpotees 0) või mitte  (1), mathlab 1
      p = %f väiksed p väärtused hüpoteesi 1 poolt
      k = %.5f
      c = NA kui c on suurem kui k, siis on hüpotees 0, h väärtus k ja c vahekorrast """ %
      (r[1], r[0])
      )

print("""
ei ole tegemist ei norm ega exp jaotusega hinna puhul
""")

rNorm = r = lilliefors(weight)
print("""kaal lilliefors norm:
      h = NA normaaljaotus (hüpotees 0) või mitte  (1), mathlab 1
      p = %f väiksed p väärtused hüpoteesi 1 poolt
      k = %.5f
      c = NA kui c on suurem kui k, siis on hüpotees 0, h väärtus k ja c vahekorrast 
      """ %
      (r[1], r[0])
      )
      
# there is no Alpha parameter for python 
print(' --- kaal ---')
r = lilliefors(weight, dist='exp')
print("""kaal lilliefors exp:
      h = NA normaaljaotus (hüpotees 0) või mitte  (1), mathlab 1
      p = %f väiksed p väärtused hüpoteesi 1 poolt
      k = %.5f
      c = NA kui c on suurem kui k, siis on hüpotees 0, h väärtus k ja c vahekorrast """ %
      (r[1], r[0])
      )

print("""
on tegemist norm jaotusega, kuna p=%.5f on suuurem kui k=%.5f
""" % (rNorm[1], rNorm[0]))

print("""
--- see ok, 
kuna kaal on "normaalne" aga hind on kunstlik 
""")