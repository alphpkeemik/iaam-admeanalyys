import matplotlib.pyplot as plt
from numpy import NAN
import pandas as pd

from components.independent import transform_age

df = pd.read_csv('iseseisev.csv', delimiter=';')


# püüaks vaadata kas on seos artisti esinema saamisega
# * vanusel (activesinceyear+activesincemonth - event number, va veebruaris, La juuli) ja
# * stiiilil (style    stylespecify)
# * kas on unplugged
# * kas on naislaulja singer
# * registration_country - peaks olema, sest reeglina välisartiste me kutsusime


new = []
iterate = df.iterrows()
for i, r in df.iterrows():
    new.append(transform_age(r.event, r.activesinceyear,
             r.activesincemonth, r.activesincetext))
df['age'] = new
