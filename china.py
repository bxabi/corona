import json
import pandas as pd

from Generator import tools


class China:
    mapView = []
    population = {}

    totalDeaths = {}
    lastDayDeaths = {}
    totalCases = {}
    lastDayCases = {}

    def __init__(self):
        with open('data/admin1.geojson') as json_file:
            self.geo = json.load(json_file)

        provincesCsv = pd.read_csv('data/China/provinces.csv', "\t")

        provinces = {}
        for row in provincesCsv.values:
            provinces[row[0]] = row[1]
            self.population[row[1]] = row[2] * 1000000

        with open('data/China/lastDay.json') as json_file:
            jsonLast = json.load(json_file)
        with open('data/China/prevDay.json') as json_file:
            jsonPrev = json.load(json_file)

        for element in jsonLast:
            state = provinces[element["provinceShortName"]]
            self.totalCases[state] = element["confirmedCount"]
            self.totalDeaths[state] = element["deadCount"]

        for element in jsonPrev:
            state = provinces[element["provinceShortName"]]
            self.lastDayCases[state] = self.totalCases[state] - element["confirmedCount"]
            self.lastDayDeaths[state] = self.totalDeaths[state] - element["deadCount"]

        self.geo["features"][:] = [value for value in self.geo["features"] if self.hasChineseData(value)]

    def hasChineseData(self, object):
        country = object["properties"]["country"]
        if country != "China":
            return False

        state = object["properties"]["name"]
        if state in self.population:
            pop = self.population[state]
            object["id"] = state
            row = tools.getMapviewRow(state, self.lastDayCases[state], self.lastDayDeaths[state],
                                      self.totalCases[state], self.totalDeaths[state], pop)
            self.mapView.append(row)
            return True

        print(state + " is in China but has no data")
        return False
