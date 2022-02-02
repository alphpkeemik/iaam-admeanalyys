import matplotlib.pyplot as plt
import pandas as pd
import mplcursors

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# - step 3-2 plots grouped
#-- boxblot, vuntsid
df['price'] = pd.to_numeric(df['price'])

mplcursors.cursor(hover=True)

map = {
    1: 'USA',
    2: 'EU',
    3: 'JAP',
}

df['origin'] = df['origin'].transform(lambda x: map[x] if x else NAN)

df.boxplot(column='price', by='origin')

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
