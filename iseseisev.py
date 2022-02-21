#!/usr/bin/env python3

import pandas as pd
from components.independent import transform_age, transform_style

inputFile = '/mnt/c/IAAM/ICM0031 Andmeanalüüs/iseseisev töö normaliseerimata andmed.csv'
outputFile = '/mnt/c/IAAM/ICM0031 Andmeanalüüs/iseseisev töö normaliseeritud andmed.csv'
df = pd.read_csv(inputFile, delimiter=';')

new = []
iterate = df.iterrows()
for i, r in df.iterrows():
    age = transform_age(r.event, r.activesinceyear,
                        r.activesincemonth, r.activesincetext)
    new.append(age)
df['vanus'] = new

new = []
iterate = df.iterrows()
for i, r in df.iterrows():
    style = transform_style(r.style, r.stylespecify)
    new.append(style)
df['stiil'] = new

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
df['singer'] = df['singer'].transform(transform)

df['event'] = df['event'].transform(
    lambda x: '20' + x[2:2]
)

# nimeta väljad inimloetavamaks
df = df.rename(columns={
    'selected':   'valitud esinema',
    'event': 'sündmuse aasta',
    'name': 'artisti nimi',
    'place': 'artisti kodukoht',
    'activesinceyear': 'alustamise aasta',
    'activesincemonth': 'alustamise kuu',
    'activesinceyear': 'vanus tekstina',
    'style': 'stiil klassifikaator',
    'stylespecify': 'stiil tekstina',
    'singer': 'laulja kaal',
    'registration_country': 'IP riik',
}, errors="raise")

df.drop(columns=['unplugged'])  # ei kasuta hetkel


df.to_csv(outputFile, sep=',', compression=None)
