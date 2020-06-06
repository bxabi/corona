import json
import pandas as pd
import numpy as np

from Generator import tools


class USA:
    totalDeaths = {}
    lastDayDeaths = {}
    totalCases = {}
    lastDayCases = {}
    mapView = []

    def __init__(self):
        self.population = pd.read_csv("data/USA/usa-population.csv", "\t")

        with open('data/admin1.geojson') as json_file:
            self.geo = json.load(json_file)

        csv = pd.read_csv('data/USA/us-states.csv', ',')

        for row in reversed(csv.values):
            state = row[1]
            cases = row[3]
            deaths = row[4]

            if state in self.lastDayCases:  # we parsed the last 2 days already
                break

            if state not in self.totalCases:
                self.totalCases[state] = cases
                self.totalDeaths[state] = deaths
            else:
                self.lastDayCases[state] = self.totalCases[state] - cases
                self.lastDayDeaths[state] = self.totalDeaths[state] - deaths

        self.geo["features"][:] = [value for value in self.geo["features"] if self.isInUsa(value)]

    def isInUsa(self, object):
        country = object["properties"]["country"]
        if country != "United States of America":
            return False

        state = object["properties"]["name"]
        result = np.where(self.population.State.values == state)
        if result[0].size > 0:
            object["id"] = state
            row = tools.getMapviewRow(state, self.lastDayCases[state], self.lastDayDeaths[state],
                                      self.totalCases[state], self.totalDeaths[state],
                                      self.population.Population.values[result[0][0]])
            self.mapView.append(row)
            return True

        return False
