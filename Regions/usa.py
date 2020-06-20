import json
import pandas as pd

from . import tools


class USA:
    mapView = []
    population = {}
    plotData = []

    totalDeaths = {}
    lastDayDeaths = {}
    totalCases = {}
    lastDayCases = {}

    def __init__(self):
        populationCsv = pd.read_csv("data/USA/usa-population.csv", ",")
        for row in populationCsv.values:
            self.population[row[0]] = row[1]
            self.totalCases[row[0]] = 0
            self.totalDeaths[row[0]] = 0

        with open('data/admin1.geojson') as json_file:
            self.geo = json.load(json_file)

        csv = pd.read_csv('data/USA/us-states.csv', ',')

        for row in csv.values:
            state = row[1]
            cases = row[3]
            deaths = row[4]

            if state not in self.population:
                continue  # Guam, Northern Mariana Islands, Virgin Islands.
            else:
                pop = self.population[state]

            self.lastDayCases[state] = cases - self.totalCases[state]
            self.lastDayDeaths[state] = deaths - self.totalDeaths[state]
            self.totalCases[state] = cases
            self.totalDeaths[state] = deaths

            deathsPerPopulation = deaths * 100 / pop
            dailyDeathsPerPopulation = self.lastDayDeaths[state] * 100 / pop  # how many %
            casesPerPopulation = cases * 100 / pop
            dailyCasesPerPopulation = self.lastDayCases[state] * 100 / pop  # how many %

            self.plotData.append(
                {"country": state, "date": row[0],
                 "newCases": self.lastDayCases[state],
                 "newDeaths": self.lastDayDeaths[state], "totalCases": cases,
                 "totalDeaths": deaths, "deathsPerPopulation": deathsPerPopulation,
                 "casesPerPopulation": casesPerPopulation,
                 "dailyDeathsPerPopulation": dailyDeathsPerPopulation,
                 "dailyCasesPerPopulation": dailyCasesPerPopulation})

        self.geo["features"][:] = [value for value in self.geo["features"] if self.isInUsa(value)]

    def isInUsa(self, object):
        country = object["properties"]["country"]
        if country != "United States of America":
            return False

        state = object["properties"]["name"]
        if state in self.population:
            object["id"] = state
            row = tools.getMapviewRow(state, self.lastDayCases[state], self.lastDayDeaths[state],
                                      self.totalCases[state], self.totalDeaths[state],
                                      self.population[state])
            self.mapView.append(row)
            return True

        return False
