import pandas as pd

from . import tools


class World:
    data = []
    mapView = []
    population = {}

    def __init__(self):
        populationData = pd.read_csv('data/population.csv', '\t')
        for line in populationData.values:
            pop = int(line[77].replace(' ', ''))
            if pop >= 100:
                self.population[line[2].upper()] = pop
            else:
                self.population[line[2].upper()] = -1
            #    print("Too small population: " + line[2])

        alldata = pd.read_csv('data/COVID-19-worldwide.csv')
        for line in alldata.values:
            self.data.append({'date': line[0], 'newDeaths': line[5], 'country': line[6].upper().replace('_', ' '),
                              'population': line[9], 'newCases': line[4]})
        self.data.reverse()

        totalDeaths = 0
        totalCases = 0
        last = ''
        index = 0
        while index < len(self.data):
            current = self.data[index]
            if current['country'] != last:  # data for a new country starts.
                last = current['country']
                totalDeaths = 0
                totalCases = 0
                pop = self.getPopulation(last)

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
                if index == len(self.data) - 1 or last != self.data[index + 1]['country']:
                    row = tools.getMapviewRow(last, current["newCases"], current["newDeaths"], totalCases, totalDeaths,
                                              pop * 1000)
                    self.mapView.append(row)

                index = index + 1

            else:
                self.data.__delitem__(index)

    def getPopulation(self, last):
        if last in self.population:
            pop = int(self.population[last])
            if pop == -1:  # population too small
                pop = 0
        else:
            print("Population of " + last + " is not found.")
            pop = 0
            # pop = current['population'] / 1000
        # print(last + " - UN Population:" + str(pop) + ", WB population:" + str(current['population'] / 1000))
        return pop
