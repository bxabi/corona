import json
import pandas as pd

from Generator import tools

with open('data/admin1.geojson') as json_file:
    admin1Geo = json.load(json_file)

deathByState = pd.read_csv('data/germany-deaths-by-state.csv', ',')

stateNames = {"BW": "Baden-Württemberg", "BY": "Bayern", "BE": "Berlin", "BB": "Brandenburg", "HB": "Bremen",
              "HH": "Hamburg", "HE": "Hessen", "NI": "Niedersachsen", "MV": "Mecklenburg-Vorpommern",
              "NW": "Nordrhein-Westfalen", "RP": "Rheinland-Pfalz", "SL": "Saarland", "SN": "Sachsen",
              "ST": "Sachsen-Anhalt", "SH": "Schleswig-Holstein", "TH": "Thüringen"}

population = {"BW": 11069533, "BY": 13076721, "BE": 3644826, "BB": 2511917, "HB": 682986, "HH": 1841179,
              "HE": 6265809, "NI": 7982448, "MV": 1609675,
              "NW": 17932651, "RP": 4084844, "SL": 990509, "SN": 4077937,
              "ST": 2208321, "SH": 2896712, "TH": 2143145}

totalDeaths = {}
for column in deathByState.items():
    short = column[0][3:5]
    if short in stateNames.keys():
        total = column[1].values[-1]
        totalDeaths[stateNames[short]] = total
        # print(state_map[short] + ": " + str(total))

mapView = []


def getPopulation(state):
    for key, value in stateNames.items():
        if value == state:
            return population[key]


def isInGermany(object):
    state = object["properties"]["name"]
    object["id"] = state
    if state in stateNames.values():
        row = tools.getMapviewRow(state, 0, 0, 0, totalDeaths[state], getPopulation(state))
        mapView.append(row)
        return True
    return False


admin1Geo["features"][:] = [value for value in admin1Geo["features"] if isInGermany(value)]


def loadCoronaData():
    return mapView, admin1Geo
