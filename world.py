import pandas as pd

from Generator import tools

population = {}
populationData = pd.read_csv('data/population.csv', '\t')
for line in populationData.values:
    pop = int(line[77].replace(' ', ''))
    if pop >= 100:
        population[line[2].upper()] = pop
    else:
        population[line[2].upper()] = -1
    #    print("Too small population: " + line[2])


def loadCoronaData():
    data = []
    mapView = []

    alldata = pd.read_excel('data/COVID-19-worldwide.xlsx')
    for line in alldata.values:
        data.append({'date': line[0], 'newDeaths': line[5], 'country': line[6].upper().replace('_', ' '),
                     'population': line[9], 'newCases': line[4]})
    data.reverse()

    totalDeaths = 0
    totalCases = 0
    last = ''
    index = 0
    while index < len(data):
        current = data[index]
        if current['country'] != last:  # data for a new country starts.
            last = current['country']
            totalDeaths = 0
            totalCases = 0
            pop = getPopulation(last)

        totalDeaths += current['newDeaths']
        totalCases += current['newCases']
        current['totalDeaths'] = totalDeaths
        current['totalCases'] = totalCases

        if pop > 0:
            deathsPerPopulation = totalDeaths * 100 / (pop * 1000)
            current['deathsPerPopulation'] = deathsPerPopulation  # how many %
            current['dailyDeathsPerPopulation'] = current['newDeaths'] * 100 / (pop * 1000)  # how many %

            casesPerPopulation = totalCases * 100 / (pop * 1000)
            current['casesPerPopulation'] = casesPerPopulation  # how many %
            current['dailyCasesPerPopulation'] = current['newCases'] * 100 / (pop * 1000)  # how many %

            # store the last value for the map view.
            if index == len(data) - 1 or last != data[index + 1]['country']:
                row = tools.getMapviewRow(last, current["newCases"], current["newDeaths"], totalCases, totalDeaths,
                                          pop * 1000)
                mapView.append(row)

            index = index + 1

        else:
            data.__delitem__(index)

    return data, mapView


def getPopulation(last):
    if last in population:
        pop = int(population[last])
        if pop == -1:  # population too small
            pop = 0
    else:
        print("Population of " + last + " is not found.")
        pop = 0
        # pop = current['population'] / 1000
    # print(last + " - UN Population:" + str(pop) + ", WB population:" + str(current['population'] / 1000))
    return pop
