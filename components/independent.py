
from cmath import isnan
import json
from pickle import POP
from numpy import NaN
from pandas import isnull
import re
import requests

rYearsInt = re.compile("(\d+)\.?(a|aastat|year|years)")
rYearsFfoat = re.compile("^u?\.?\s?(\d)[,\.](\d)(\s|\.)?(a|aastat)\.?$")
rMonths = re.compile("(\d\d?)\.?kuud")
rYear = re.compile("20\d\d|19\d\d")
rEventYear = re.compile("\d\d$")
rPlainInt = re.compile("^\d\d?$")
rCleanup = re.compile('about|umbes|less|than|~|\s')
ageMap = {
    "Aastajavähepeale!:)": 1.1,
    "poolaastat": 0.5,
    "aasta": 1,
    "0,75": 0.75,
    "aasta??..": 1,
    "peaaeguaasta": .9,
    "üsnamituaastat": 3,
    "kaksjapoolaastat": 2.5,
    "Ükskomapool(1,5mhmh)": 1.5,
    "Pronksöölsündinud": "2007",
    "kaheaasta,pausidega": 2,
    "kaksjapoolaastat": 2.5,
    "poolteistaastat": 1.5,
    "saablellealternatiivilviisaastat": 5,
    "juulistäitubaasta": 1,
    "alatesnaistepäevast'94": "1994",
    "½ayear": .5,
    "oneyear": 1,
    "poolaastat": 0.5,
    "Saimejustkolmeseks:)": 3,
    "around1": 1,
    "ayear": 1,
    "Hetkelaasta": 1,
    "Ükskomaviisaastat": 1.5,
    "1,5": 1.5,
    "Aasta": 1,
    "08sügisest": "2008",
    "3-4": 3.5,
    "poolaastat": 0.5,
    "aasta": 1,
    "paaraastat": 2,
}


def transform_age(event, activesinceyear, activesincemonth, activesincetext):
    if isnan(activesinceyear) == False:
        y = rEventYear.search(event)
        years = int('20' + y.group(0)) - activesinceyear
        if isnan(activesincemonth) == False:
            return years + activesincemonth/12
        return years

    if isnull(activesincetext) == True:
        return NaN

    activesincetext = activesincetext.strip().replace("üle", '')
    activesincetext = rCleanup.sub('', activesincetext)

    # full yar
    x = rYear.search(activesincetext)
    if x:
        y = rEventYear.search(event)

        return int('20' + y.group(0)) - int(x.group(0))

    # plain number
    x = rPlainInt.match(activesincetext)
    if x:
        return int(x.group(0))

    # 1.5 ...
    x = rYearsFfoat.match(activesincetext)
    if x:
        return int(x.group(1)) + int(x.group(2))/10

    mMonths = rMonths.search(activesincetext)
    x = rYearsInt.search(activesincetext)
    if x:
        if mMonths:
            return int(x.group(1)) + int(mMonths.group(1))/12
        return int(x.group(1))

    if mMonths:
        return int(mMonths.group(1))/12

    if activesincetext in ageMap:
        activesincetext = ageMap[activesincetext]
        if isinstance(activesincetext, str) == False:
            return activesincetext

    return NaN


ROCK = "Rock"
PUNK = "Punk"
METAL = "Metal"
MUU = "Muu"
FOLK = "Folk"
POPP = "Popp"
ELEKTROONILINE = "Elektrooniline"
EKSPERIMENTAALNE = "Eksperimentaalne"
JAZZ = "Jazz"
HIP_HOP = "HipHop"


styleMap = {
    "põrkepunk": PUNK,
    "Alternatiiv": EKSPERIMENTAALNE,
    "Pop/Rock/Alernative": ROCK,
    "Rock": ROCK,
    "Keldri": EKSPERIMENTAALNE,
    "Hard rock": ROCK,
    "Klassikaline Rock": ROCK,
    "Elektropunkrokk": PUNK,
    "alternatiivne pop punkrock": PUNK,
    "Melodic Metal": METAL,
    "Indie, Alternatiivrokk": MUU,
    "indiemonkeyfunkeyreggaedrumandbass": MUU,
    "Mahe ja meeldiv": MUU,
    "Alternatiivne": MUU,
    "Soul/Rock": ROCK,
    "Doom": METAL,
    "Ökometal": METAL,
    "Hard/Glam Rock": METAL,
    "skapunk": PUNK,
    "Thrashy alternative metal": METAL,
    "Funky Indie-rokk": MUU,
    "Freaky:Rock": MUU,
    "indie rock folk,grunge ning elektroonilisete mõjutustega": MUU,
    "Lo Fi": ELEKTROONILINE,
    "hardcore / groove metal": METAL,
    "pop punk/powerpop": POPP,
    "Popp-rokk-kantri-rege-bluus": POPP,
    "Hardcore / Electro / Punk": ELEKTROONILINE,
    "Gooti Nu": MUU,
    "stoner/riff/metal": METAL,
    "pagan metal": METAL,
    "indie / rock": ROCK,
    "Garage, Alternative": EKSPERIMENTAALNE,
    "Ska, Hardcore": MUU,
    "Progressive": MUU,
    "Alternative punkrock": EKSPERIMENTAALNE,
    "Melodic Deathcore": MUU,
    "Rock/psühhedeelia/punk": ROCK,
    "funk/ska/pop": POPP,
    "Triprock": ROCK,
    "stoner": MUU,
    "Alternative Punk": PUNK,
    "Surf-Psych": MUU,
    "Protopunk/Psychedelic hardrock": METAL,
    "post-folk": FOLK,
    "Riffenroll": MUU,
    "Alternatiiv rokk": ROCK,
    "Träss": MUU,
    "Drive": MUU,
    "Dance Punk": PUNK,
    "Grindcore": MUU,
    "Post Hardcore, Punk": PUNK,
    "Progressive death/doom": METAL,
    "Isevalminud stiil, võimalik, et Indie": MUU,
    "Reggae, punk, ska, rock": MUU,
    "...,rock,metal...": METAL,
    "Punk-Rock": PUNK,
    "we call it dance rock": ROCK,
    "Hard-Rock": ROCK,
    "Alternative": MUU,
    "Alternatiivrock": ROCK,
    "sõidu-seiklus&seisundimuusika": MUU,
    "Progressiivne": EKSPERIMENTAALNE,
    "Metalcore": METAL,
    "Torerock": ROCK,
    "post-hardcore/metalcore": METAL,
    "Electro/metalcore": METAL,
    "Alternative rock": ROCK,
    "Garaaž": ROCK,
    "Metalcore/post-hardcore": METAL,
    "Alternative Pop/Rock": ROCK,
    "hard rock/heavy metal": METAL,
    "Death metal/Experimental": METAL,
    "glam / new wave": EKSPERIMENTAALNE,
    "Disco | Rock | Svensk podiet": ROCK,
    "Sarcastic": MUU,
    "Alternatiiv rocki, rocki, pop-rocki hübriid, meelodilise vokaliga.": ROCK,
    "Bluus-rock": ROCK,
    "Alternatiiv/Post": MUU,
    "Celtic punk": PUNK,
    "Sludge Metal": METAL,
    "Melodic Death Metal": METAL,
    "Jazz, Ambient, Jazz-Rock": ROCK,
    "Death metal / hardcore": METAL,
    "hard rock, hair metal": METAL,
    "Indie": MUU,
    "Riff-driven modern metal": METAL,
    "Crossover rock": ROCK,
    "groove/death metal": METAL,
    "Post-hardcore/electronica": ELEKTROONILINE,
    "Haigism": MUU,
    "D-beat/Hardcore/Crust Punk Doom'i ja Sludge'i elementidega": METAL,
    "progressive hard rock pop": ROCK,
}


def transform_style(style, stylespecify):
    if style == 'Hip Hop':
        return HIP_HOP
    if isnull(style) == False:
        return style

    if stylespecify in styleMap:
        return styleMap[stylespecify]

    return 'stiil_m22ramata'


ipMapFilePath = './data/ipdata.json'
ipMapFile = open(ipMapFilePath)
ipMap = json.load(ipMapFile)

bandCountry = {
    "The Lost Highway": "EE",
    "Canis Lupus": "EE",
    "die moritz": "EE",
    "Pimpfish": "EE",
    "Taak": "EE",
    "Vaiko Eplik ja Eliit": "EE",
    "Vespera": "US",
    "Aides": "EE",
    "Mikk ja Marko": "EE",
    "Dr. Hell Hambaravi": "EE",
    "Adjusted": "EE",
    "Bird People": "SE",
    "The Happs'": "LV",
    "The Flowers of Romance": "EE",
    "Ambrosia": "LV",
    "Tarkmeenia": "EE",
    "LEEK": "EE",
    "Boom Truck": "EE",
    "Johnny masturbates in yellow bed": "EE",
    "Edgar Poe's Favorite Cat": "EE",
    "Talisman": "EE",
    "Under Wunder": "EE",
}


def transform_country(country, ip, place, name):

    if name in bandCountry:
        return bandCountry[name]
    if country == 'RD':
        return 'EE'

    if isnull(country) == False:
        return country

    if isnull(ip) == False:
        if ip in ipMap:
            if isnull(ipMap[ip]) == False:
                return ipMap[ip]
        else:
            print(ip)
            url = 'http://ip-api.com/json/' + ip
            resp = requests.get(url=url)
            data = resp.json()

            ipMap[ip] = data.get('countryCode')

            with open(ipMapFilePath, "w") as outfile:
                json.dump(ipMap, outfile)
    if place in ('Tallinn', 'Kallaste', 'TAL'):
        return 'EE'
    return 'riik_teadmata'
