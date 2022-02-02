import matplotlib.pyplot as plt
import pandas as pd
import mplcursors

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# - step 3 plots
#-- boxblot, vuntsid
df['price'] = pd.to_numeric(df['price'])

mplcursors.cursor(hover=True)

fig = plt.figure()

df.boxplot(column='price')
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html 
#df.boxplot(column='price', whis=0)

# anntoations


def showLabel(sel):
    value = df[df['price'] == sel.target[1]][['make', 'model', 'price']]
    if value.size:
        sel.annotation.set_text(
            'Point {}'.format(value)
        )
    else:
        sel.annotation.set_text(
            'Value {}'.format(sel.target[1].round(2))
        )


crs = mplcursors.cursor(hover=True)
crs.connect("add", showLabel)
plt.show()
