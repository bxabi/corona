import json
import pandas as pd
import numpy as np

from Generator import tools

with open('data/admin1.geojson') as json_file:
    admin1Geo = json.load(json_file)

provincesCsv = pd.read_csv('data/China/provinces.csv', "\t")

provinces = {}
population = {}
for row in provincesCsv.values:
    provinces[row[0]] = row[1]
    population[row[1]] = row[2] * 1000000

with open('data/China/COVID-19_2020-05-07(CN-DATA)by_DXY.json') as json_file:
    jsonLast = json.load(json_file)
with open('data/China/COVID-19_2020-05-06(CN-DATA)by_DXY.json') as json_file:
    jsonPrev = json.load(json_file)

totalDeaths = {}
lastDayDeaths = {}
totalCases = {}
lastDayCases = {}

for element in jsonLast:
    state = provinces[element["provinceShortName"]]
    totalCases[state] = element["confirmedCount"]
    totalDeaths[state] = element["deadCount"]

for element in jsonPrev:
    state = provinces[element["provinceShortName"]]
    lastDayCases[state] = totalCases[state] - element["confirmedCount"]
    lastDayDeaths[state] = totalDeaths[state] - element["deadCount"]

mapView = []


def hasChineseData(object):
    country = object["properties"]["country"]
    if country != "China":
        return False

    state = object["properties"]["name"]
    # result = np.where(population.State.values == state)
    if state in population:
        pop = population[state]
        object["id"] = state
        row = tools.getMapviewRow(state, lastDayCases[state], lastDayDeaths[state], totalCases[state],
                                  totalDeaths[state], pop)
        mapView.append(row)
        return True

    print(state +" is in China but has no data")
    return False


admin1Geo["features"][:] = [value for value in admin1Geo["features"] if hasChineseData(value)]


def loadCoronaData():
    return mapView, admin1Geo
