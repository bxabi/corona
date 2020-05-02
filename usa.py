import json
import pandas as pd
import numpy as np

from Generator import tools

population = pd.read_csv("data/USA/usa-population.csv", "\t")

with open('data/admin1.geojson') as json_file:
    admin1Geo = json.load(json_file)

csv = pd.read_csv('data/USA/usa.csv', ',')

totalDeaths = {}
lastDayDeaths = {}
totalCases = {}
lastDayCases = {}

for row in reversed(csv.values):
    state = row[1]
    cases = row[3]
    deaths = row[4]

    if state in lastDayCases:  # we parsed the last 2 days already
        break

    if state not in totalCases:
        totalCases[state] = cases
        totalDeaths[state] = deaths
    else:
        lastDayCases[state] = totalCases[state] - cases
        lastDayDeaths[state] = totalDeaths[state] - deaths

mapView = []


def isInUsa(object):
    country = object["properties"]["country"]
    if country != "United States of America":
        return False

    state = object["properties"]["name"]
    result = np.where(population.State.values == state)
    if result[0].size > 0:
        object["id"] = state
        row = tools.getMapviewRow(state, lastDayDeaths[state], lastDayDeaths[state], totalCases[state],
                                  totalDeaths[state], population.Population.values[result[0][0]])
        mapView.append(row)
        return True
    return False


admin1Geo["features"][:] = [value for value in admin1Geo["features"] if isInUsa(value)]


def loadCoronaData():
    return mapView, admin1Geo
