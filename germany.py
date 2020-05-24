import json
import pandas as pd

from Generator import tools

stateNames = {"BW": "Baden-Württemberg", "BY": "Bayern", "BE": "Berlin", "BB": "Brandenburg", "HB": "Bremen",
              "HH": "Hamburg", "HE": "Hessen", "NI": "Niedersachsen", "MV": "Mecklenburg-Vorpommern",
              "NW": "Nordrhein-Westfalen", "RP": "Rheinland-Pfalz", "SL": "Saarland", "SN": "Sachsen",
              "ST": "Sachsen-Anhalt", "SH": "Schleswig-Holstein", "TH": "Thüringen"}

population = {"BW": 11069533, "BY": 13076721, "BE": 3644826, "BB": 2511917, "HB": 682986, "HH": 1841179,
              "HE": 6265809, "NI": 7982448, "MV": 1609675,
              "NW": 17932651, "RP": 4084844, "SL": 990509, "SN": 4077937,
              "ST": 2208321, "SH": 2896712, "TH": 2143145}


def getPopulation(state):
    for key, value in stateNames.items():
        if value == state:
            return population[key]


with open('data/admin1.geojson') as json_file:
    admin1Geo = json.load(json_file)

csv = pd.read_csv('data/Germany/data.csv', ',')

totalDeaths = {}
lastDayDeaths = {}
totalCases = {}
lastDayCases = {}

data = {}

for column in csv.items():
    short = column[0][3:5]
    if short in stateNames.keys():
        state = stateNames[short]
        total = column[1].values[-1]
        last = total - column[1].values[-2]
        t = column[0][6:]
        if t == "cases":
            totalCases[state] = total
            lastDayCases[state] = last
            data[state] = []
            for i in range(1, len(column[1].values)):
                data[state].append({})
                data[state][i - 1]["totalCases"] = column[1].values[i]
                data[state][i - 1]["lastDayCases"] = column[1].values[i] - column[1].values[i - 1]
        else:
            totalDeaths[state] = total
            lastDayDeaths[state] = last
            for i in range(1, len(column[1].values)):
                data[state][i - 1]["totalDeaths"] = column[1].values[i]
                data[state][i - 1]["lastDayDeaths"] = column[1].values[i] - column[1].values[i - 1]

plotData = []
items = next(csv.items())
for state in stateNames.values():
    pop = getPopulation(state)
    for i in range(0, len(data[state])):  # date column
        current = data[state][i]
        deathsPerPopulation = current["totalDeaths"] * 100 / pop
        dailyDeathsPerPopulation = current["lastDayDeaths"] * 100 / pop  # how many %

        casesPerPopulation = current["totalCases"] * 100 / pop
        dailyCasesPerPopulation = current["lastDayCases"] * 100 / pop  # how many %

        plotData.append({"country": state, "date": items[1].values[i+1],  # 0'th column, 1 is the values part.
                         "newCases": current["lastDayCases"],
                         "newDeaths": current["lastDayDeaths"], "totalCases": current["totalCases"],
                         "totalDeaths": current["totalDeaths"], "deathsPerPopulation": deathsPerPopulation,
                         "casesPerPopulation": casesPerPopulation, "dailyDeathsPerPopulation": dailyDeathsPerPopulation,
                         "dailyCasesPerPopulation": dailyCasesPerPopulation})

    mapView = []


    def isInGermany(object):
        country = object["properties"]["country"]
        if country != "Germany":
            return False

        state = object["properties"]["name"]
        if state in stateNames.values():
            object["id"] = state
            row = tools.getMapviewRow(state, lastDayCases[state], lastDayDeaths[state], totalCases[state],
                                      totalDeaths[state], getPopulation(state))
            mapView.append(row)
            return True
        return False


    admin1Geo["features"][:] = [value for value in admin1Geo["features"] if isInGermany(value)]


    def loadCoronaData():
        return mapView, admin1Geo, plotData
