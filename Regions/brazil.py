import json
import pandas as pd

from . import tools


class Brazil:
    mapView = []
    states = {}
    population = {}

    totalDeaths = {}
    lastDayDeaths = {}
    totalCases = {}
    lastDayCases = {}

    plotData = []

    def __init__(self):
        statesCsv = pd.read_csv("data/Brazil/states.csv", ",")

        for row in statesCsv.values:
            self.states[row[0]] = row[1]
            self.population[row[1]] = row[2]

        with open('data/admin1.geojson') as json_file:
            self.geo = json.load(json_file)

        csv = pd.read_csv('data/Brazil/cases-brazil-states.csv')

        for row in csv.values:
            if row[2] == 'TOTAL':  # skip values for the whole country
                continue

            short = row[2]
            state = self.states[short]

            date = row[0]
            tc = int(row[7])
            ldc = int(row[6])
            td = int(row[5])
            ldd = int(row[4])
            pop = self.population[state]

            deathsPerPopulation = td * 100 / pop
            dailyDeathsPerPopulation = ldd * 100 / pop  # how many %
            casesPerPopulation = tc * 100 / pop
            dailyCasesPerPopulation = ldc * 100 / pop  # how many %
            self.plotData.append({"country": state, "date": date,
                                  "newCases": ldc, "newDeaths": ldd, "totalCases": tc,
                                  "totalDeaths": td, "deathsPerPopulation": deathsPerPopulation,
                                  "casesPerPopulation": casesPerPopulation,
                                  "dailyDeathsPerPopulation": dailyDeathsPerPopulation,
                                  "dailyCasesPerPopulation": dailyCasesPerPopulation})
            self.lastDayCases[state] = ldc
            self.lastDayDeaths[state] = ldd
            self.totalCases[state] = tc
            self.totalDeaths[state] = td

        self.geo["features"][:] = [value for value in self.geo["features"] if self.isInBrazil(value)]

    def isInBrazil(self, object):
        country = object["properties"]["country"]
        if country != "Brazil":
            return False

        state = object["properties"]["name"]
        if state in self.states.values():
            object["id"] = state
            row = tools.getMapviewRow(state, self.lastDayCases[state], self.lastDayDeaths[state],
                                      self.totalCases[state], self.totalDeaths[state], self.population[state])
            self.mapView.append(row)
            return True

        return False
