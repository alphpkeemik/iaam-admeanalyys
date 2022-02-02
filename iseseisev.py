import matplotlib.pyplot as plt
from numpy import NAN
import pandas as pd
import mplcursors

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
    age = transform_age(r.event, r.activesinceyear,
                        r.activesincemonth, r.activesincetext)
    new.append(age)
df['age'] = new

df['selected'] = df['selected'].transform(
    lambda x: 'yes' if x == 1 else 'no'
)

df = df[df['age']>0]
df.boxplot(column='age', by='selected')
ax = plt.subplot(111)
#ax.set_ylabel('age', loc='bottom')
# anntoations


def showLabel(sel):
    value = df[df['age'] == sel.target[1]][[
        'id', 'age', 'event',
        'activesinceyear',
        'activesincemonth',
        'activesincetext',
    ]]
    if value.size:
        sel.annotation.set_text(
            'Point {}'.format(value)
        )
    else:
        sel.annotation.set_text(
            'Value {}'.format(sel.target[1].round(2))
        )


mplcursors.cursor(hover=True)
crs = mplcursors.cursor(hover=True)
crs.connect("add", showLabel)
plt.show()
