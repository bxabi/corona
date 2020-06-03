import json
import pandas as pd

from Generator import tools

statesCsv = pd.read_csv("data/Brazil/states.csv", ",")

states = {}
population = {}
for row in statesCsv.values:
    states[row[0]] = row[1]
    population[row[1]] = row[2]

with open('data/admin1.geojson') as json_file:
    admin1Geo = json.load(json_file)

csv = pd.read_csv('data/Brazil/cases-brazil-states.csv')

totalDeaths = {}
lastDayDeaths = {}
totalCases = {}
lastDayCases = {}

plotData = []

ldc = 0
ldd = 0
tc = 0
td = 0

for row in csv.values:
    if row[2] == 'TOTAL':  # skip values for the whole country
        continue

    short = row[2]
    state = states[short]

    date = row[0]
    tc = int(row[7])
    ldc = int(row[6])
    td = int(row[5])
    ldd = int(row[4])
    pop = population[state]

    deathsPerPopulation = td * 100 / pop
    dailyDeathsPerPopulation = ldd * 100 / pop  # how many %
    casesPerPopulation = tc * 100 / pop
    dailyCasesPerPopulation = ldc * 100 / pop  # how many %
    plotData.append({"country": state, "date": date,
                     "newCases": ldc, "newDeaths": ldd, "totalCases": tc,
                     "totalDeaths": td, "deathsPerPopulation": deathsPerPopulation,
                     "casesPerPopulation": casesPerPopulation, "dailyDeathsPerPopulation": dailyDeathsPerPopulation,
                     "dailyCasesPerPopulation": dailyCasesPerPopulation})
    lastDayCases[state] = ldc
    lastDayDeaths[state] = ldd
    totalCases[state] = tc
    totalDeaths[state] = td

mapView = []


def isInBrazil(object):
    country = object["properties"]["country"]
    if country != "Brazil":
        return False

    state = object["properties"]["name"]
    if state in states.values():
        object["id"] = state
        row = tools.getMapviewRow(state, lastDayCases[state], lastDayDeaths[state], totalCases[state],
                                  totalDeaths[state], population[state])
        mapView.append(row)
        return True
    return False


admin1Geo["features"][:] = [value for value in admin1Geo["features"] if isInBrazil(value)]


def loadCoronaData():
    return mapView, admin1Geo, plotData
