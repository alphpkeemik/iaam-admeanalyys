
from cmath import isnan
from numpy import NaN
from pandas import isnull
import re

rYearsInt = re.compile("(\d+)\.?(a|aastat|year|years)")
rYearsFfoat = re.compile("^u?\.?\s?(\d)[,\.](\d)(\s|\.)?(a|aastat)\.?$")
rMonths = re.compile("(\d\d?)\.?kuud")
rYear = re.compile("20\d\d|19\d\d")
rEventYear = re.compile("\d\d$")
rPlainInt = re.compile("^\d\d?$")
rCleanup = re.compile('about|umbes|less|than|~|\s')
map = {
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

    if activesincetext in map:
        activesincetext = map[activesincetext]
        if isinstance(activesincetext, str) == False:
            return activesincetext

    return NaN
