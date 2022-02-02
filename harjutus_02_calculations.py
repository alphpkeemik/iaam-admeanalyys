import pandas as pd

df = pd.read_csv('harjutus_01_autod.csv', delimiter=';')
df = df.rename(columns=lambda x: x.strip())
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# - step 2 calculations
# -- mean - keskmine
print('mean with NAN: ', df['mpg'].mean())
# -- for skipping NANs
df['mpg'] = pd.to_numeric(df['mpg'])
df['price'] = pd.to_numeric(df['price'])

print('mean no nan: ', df['mpg'].mean())

# -- mode - esineb kõige sagedamine:
print('mode: ', df['mpg'].mode())

print('mpg=21 arv: ', df[df['mpg'] == 21].size)

# -- median - pooled väärtused suuremad, pooled väiksemad
print('median: ', df['mpg'].median())
# -- kvantiilid (kvartal,  veerand):
# --- mediaan ongi 0.5 kvanttil
print('kvantiil 0.5:', df['mpg'].quantile(0.5))
# --- alumine kvartal
print('kvantiil 0.25:', df['mpg'].quantile(0.25))
# --- hajuvus - vahemikku 5 peab mahtuma pooled
print('hajuvusmõõdik: ', df['mpg'].quantile(0.75) - df['mpg'].quantile(0.25))
# -- standardhälve
print('standardhälve mpg: ', df['mpg'].std().round(4))
# --- mathlab show 1.0e+04 *
print(">> standardhälve 1.0e+04 *:")
print(
    df[["mpg", "price"]].std()
    .transform(lambda x: x / 10000),
    '<<'
)

# -- indeksid kus absoluutväärtus
keskmine_hind = df.price.mean()
halve_hind = df.price.std()
print('keskmine hind: ', keskmine_hind)
print('hälve hind: ', halve_hind)

# --- autod mis langesid keskhälvest väljaspoole
print(
    'hinna keskhälvest väljaspoole: %d' %
    len(df[abs(df.price - keskmine_hind) > halve_hind])
)
print(
    'hinna keskhälvest väljaspoole 2 sigma keskmise ümber*: ',
    len(df[abs(df.price - keskmine_hind) > 2*halve_hind])
)
print(
    'hinna keskhälvest väljaspoole 3 sigma keskmise ümber*: ',
    df[abs(df.price - keskmine_hind) > 3 *
       halve_hind][['make', 'model', 'price']]
)
