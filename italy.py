import json
import pandas as pd
import numpy as np
from mako.filters import trim

from Generator import tools

with open('data/Italy/italy-regions.geojson') as json_file:
    admin1Geo = json.load(json_file)

populationCsv = pd.read_csv('data/Italy/population.csv', ",")

population = {}
for row in populationCsv.values:
    population[row[0]] = row[1]

csvLast = pd.read_csv('data/Italy/last.csv', ",")
csvPrev = pd.read_csv('data/Italy/prev.csv', ",")

totalDeaths = {}
lastDayDeaths = {}
totalCases = {}
lastDayCases = {}

for row in csvLast.values:
    state = row[3]
    totalCases[state] = row[15]
    totalDeaths[state] = row[14]

for row in csvPrev.values:
    state = row[3]
    lastDayCases[state] = totalCases[state] - row[15]
    lastDayDeaths[state] = totalDeaths[state] - row[14]

totalCases["P.A. Trento | P.A. Bolzano"] = totalCases["P.A. Trento"] + totalCases["P.A. Bolzano"];
del totalCases["P.A. Trento"]
del totalCases["P.A. Bolzano"]
totalDeaths["P.A. Trento | P.A. Bolzano"] = totalDeaths["P.A. Trento"] + totalDeaths["P.A. Bolzano"];
del totalDeaths["P.A. Trento"]
del totalDeaths["P.A. Bolzano"]
lastDayCases["P.A. Trento | P.A. Bolzano"] = lastDayCases["P.A. Trento"] + lastDayCases["P.A. Bolzano"];
del lastDayCases["P.A. Trento"]
del lastDayCases["P.A. Bolzano"]
lastDayDeaths["P.A. Trento | P.A. Bolzano"] = lastDayDeaths["P.A. Trento"] + lastDayDeaths["P.A. Bolzano"];
del lastDayDeaths["P.A. Trento"]
del lastDayDeaths["P.A. Bolzano"]

mapView = []

for object in admin1Geo["features"]:
    region = object["properties"]["name"]
    if region in lastDayCases:
        pop = population[region]
        object["id"] = region
        row = tools.getMapviewRow(region, lastDayCases[region], lastDayDeaths[region], totalCases[region],
                                  totalDeaths[region], pop)
        mapView.append(row)
    else:
        print("Population of " + region + " region in Italy is not known")

    # if province:  # is not null
    # pop = 1
    # object["id"] = province
    # row = tools.getMapviewRow(province, 1, 1, 1, 1, pop)
    # mapView.append(row)
    # return True


# admin1Geo["features"][:] = [value for value in admin1Geo["features"] if inItaly(value)]


def loadCoronaData():
    return mapView, admin1Geo
