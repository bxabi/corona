import json
import pandas as pd

from . import tools


class Russia:
    mapView = []
    statesByName = {}

    totalDeaths = {}
    lastDayDeaths = {}
    totalCases = {}
    lastDayCases = {}

    def __init__(self):
        with open('data/admin1.geojson') as json_file:
            self.geo = json.load(json_file)

        stateCsv = pd.read_csv('data/Russia/population.csv', "\t")

        statesById = {}
        for row in stateCsv.values:
            self.statesByName[row[1]] = {"id": row[0], "population": row[7]}
            statesById[row[0]] = row[1]

        csvLast = pd.read_csv('data/Russia/last.csv', ",")
        csvPrev = pd.read_csv('data/Russia/prev.csv', ",")

        for row in csvLast.values:
            if row[0] < 99:
                state = statesById[row[0]]
                self.totalCases[state] = row[1]
                self.totalDeaths[state] = row[3]

        for row in csvPrev.values:
            if row[0] < 99:
                state = statesById[row[0]]
                self.lastDayCases[state] = self.totalCases[state] - row[1]
                self.lastDayDeaths[state] = self.totalDeaths[state] - row[3]

        self.geo["features"][:] = [value for value in self.geo["features"] if self.inRussia(value)]

    def inRussia(self, object):
        country = object["properties"]["country"]
        if country != "Russia":
            return False

        state = object["properties"]["name"]
        if state in self.statesByName:
            pop = self.statesByName[state]["population"]
            object["id"] = state
            row = tools.getMapviewRow(state, self.lastDayCases[state], self.lastDayDeaths[state],
                                      self.totalCases[state], self.totalDeaths[state], pop)
            self.mapView.append(row)
            return True

        if state:  # is not null
            print(state + " is in Russia but population not found")
            # pop = 1
            # object["id"] = state
            # row = tools.getMapviewRow(state, 1, 1, 1, 1, pop)
            # mapView.append(row)
            # return True

        return False
