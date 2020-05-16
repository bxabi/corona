import json
import pandas as pd
import numpy as np

from Generator import tools

with open('data/admin1.geojson') as json_file:
    admin1Geo = json.load(json_file)

stateCsv = pd.read_csv('data/Russia/population.csv', "\t")

statesByName = {}
statesById = {}
for row in stateCsv.values:
    statesByName[row[1]] = {"id": row[0], "population": row[7]}
    statesById[row[0]] = row[1]

csvLast = pd.read_csv('data/Russia/last.csv', ",")
csvPrev = pd.read_csv('data/Russia/prev.csv', ",")

totalDeaths = {}
lastDayDeaths = {}
totalCases = {}
lastDayCases = {}

for row in csvLast.values:
    if row[0] < 99:
        state = statesById[row[0]]
        totalCases[state] = row[1]
        totalDeaths[state] = row[3]

for row in csvPrev.values:
    if row[0] < 99:
        state = statesById[row[0]]
        lastDayCases[state] = totalCases[state] - row[1]
        lastDayDeaths[state] = totalDeaths[state] - row[3]

mapView = []


def inRussia(object):
    country = object["properties"]["country"]
    if country != "Russia":
        return False

    state = object["properties"]["name"]
    if state in statesByName:
        pop = statesByName[state]["population"]
        object["id"] = state
        row = tools.getMapviewRow(state, lastDayCases[state], lastDayDeaths[state], totalCases[state],
                                  totalDeaths[state], pop)
        mapView.append(row)
        return True

    if state:  # is not null
        print(state + " is in Russia but population not found")
        # pop = 1
        # object["id"] = state
        # row = tools.getMapviewRow(state, 1, 1, 1, 1, pop)
        # mapView.append(row)
        # return True

    return False


admin1Geo["features"][:] = [value for value in admin1Geo["features"] if inRussia(value)]


def loadCoronaData():
    return mapView, admin1Geo
