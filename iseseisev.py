#!/usr/bin/env python3

from matplotlib.pyplot import pause
import pandas as pd
from components.independent import transform_age, transform_country, transform_style
import csv

path = '/mnt/c/IAAM/ICM0031 Andmeanalüüs/iseseisev/'
inputFile = path + 'raw.csv'
df = pd.read_csv(inputFile)

new = []
for i, r in df.iterrows():
    age = transform_age(r.event, r.activesinceyear,
                        r.activesincemonth, r.activesincetext)
    if type(age) == float:
        age = round(age, 1)
    if(age < 0.1):
        age = 0.1

    new.append(age)
df['vanus'] = new

new = []
for i, r in df.iterrows():
    value = transform_style(r.style, r.stylespecify)
    new.append(value)
df['stiil'] = new

new = []
for i, r in df.iterrows():
    value = transform_country(r.registration_country, r.ip, r.place, r['name'])
    new.append(value)
df['riik'] = new

df['selected'] = df['selected'].transform(
    lambda x: 'jah' if x == 1 else 'ei'
)


def transform(singer):
    if singer == 'woman':
        return 2
    if singer == 'womanandman':
        return 2
    if singer == 'other':
        return 1
    if singer == 'man':
        return 1


df['laulja'] = df['singer'].transform(transform)

df['event'] = df['event'].transform(
    lambda x: '20' + x[2:4]
)

# collect sets
countries = []
styles = []
singers = []
for i, r in df.iterrows():
    if False == (r.riik in countries):
        countries.append(r.riik)
    if False == (r.stiil in styles):
        styles.append(r.stiil)
    if False == pd.isnull(r.singer) and False == (r.singer in singers):
        singers.append(r.singer)
singers.append('laulja_m22ramata')
countries.sort()

# selectedByYear
new = {}
for i, r in df.iterrows():
    if False == (r.event in new):
        new[r.event] = {
            'aasta': r.event,
            'valitud': 0,
            'registreerunud': 0,
        }
        for v in styles:
            new[r.event][v] = 0
        for v in countries:
            new[r.event][v] = 0
            new[r.event][v] = 0
        for v in singers:
            new[r.event][v] = 0
    new[r.event]['registreerunud'] += 1
    new[r.event][r.riik] += 1
    new[r.event][r.stiil] += 1
    if r.selected == 'jah':
        new[r.event]['valitud'] += 1
        new[r.event]['kohale'] = round(
            new[r.event]['registreerunud']/new[r.event]['valitud'], 1
        )
    if pd.isnull(r.singer):
        new[r.event]['laulja_m22ramata'] += 1
    else:
        new[r.event][r.singer] += 1


ndf = pd.DataFrame.from_records(list(new.values()))
ndf.to_csv(path + 'gAll.csv', compression=None)


# nimeta väljad inimloetavamaks
df = df.rename(columns={
    'selected':   'valitud',
    'event': 'aasta',
    'name': 'nimi',
    'place': 'kodukoht',
    'activesinceyear': 'alustamise_aasta',
    'activesincemonth': 'alustamise_kuu',
    'activesincetext': 'vanus tekstina',
    'style': 'stiil klassifikaator',
    'stylespecify': 'stiil tekstina',
    'singer': 'laulja',
    'registration_country': 'IP riik',
}, errors="raise")

df = df.drop(columns=['unplugged'])  # ei kasuta hetkel

df.to_csv(path + 'data.csv', compression=None)

years = ['2007', '2008', '2009', '2010']
sep = "\t"
print(sep + sep.join(years))

for data_name, _df in {'kõik': df, 'registreerunud': df[df['valitud'] == 'jah']}.items():
    rows = []
    functions = {
        'Aritmeetiline keskmine': lambda year: '%.1f' % (_df[_df['aasta'] == year].vanus.mean()),
        'Mood': lambda year: '%.1f' % (_df[_df['aasta'] == year].vanus.mode()[0]),
        'Mediaan': lambda year: '%.1f' % (_df[_df['aasta'] == year].vanus.median()),
    }

    f = open(path + 'arvnäitajad-' + data_name + '.csv', 'w')
    writer = csv.writer(f)
    writer.writerow([''] + years)

    for name, function in functions.items():
        row = [name]
        for year in years:
            pass
            row.append(function(year))
        print(sep.join(row))
        writer.writerow(row)
    f.close()

    rows = []
    functions = {
        'Standardhälve': lambda year: '%.1f' % (_df[_df['aasta'] == year].vanus.std()),
        'Ülemine kvartiil': lambda year: '%.1f' % (_df[_df['aasta'] == year].vanus.quantile(0.25)),
        'Alumine kvartiil': lambda year: '%.1f' % (_df[_df['aasta'] == year].vanus.quantile(0.75)),
        'Kvartiilide vahe': lambda year: '%.1f' % (_df[_df['aasta'] == year].vanus.quantile(0.75) - _df[_df['aasta'] == year].vanus.quantile(0.25)),
    }
    sep = "\t"
    f = open(path + 'hajuvused-' + data_name + '.csv', 'w')
    writer = csv.writer(f)
    writer.writerow([''] + years)

    for name, function in functions.items():
        row = [name]
        for year in years:
            pass
            row.append(function(year))
        print(sep.join(row))
        writer.writerow(row)
    f.close()
