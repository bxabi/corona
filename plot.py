import plotly.express as px

import pandas as pd


class CoronaPlot:
    def __init__(self):
        self.population = {}
        self.data = []
        self.mapView = []
        self.orderedCountries = []

        self.loadPopulation()
        self.loadCoronaData()

    def loadPopulation(self):
        populationData = pd.read_csv('data/population.csv', '\t')
        for line in populationData.values:
            pop = int(line[77].replace(' ', ''))
            if pop >= 100:
                self.population[line[2].upper()] = pop
            # else:
            #     print("Too small population: " + line[2])

    def loadCoronaData(self):
        alldata = pd.read_excel('data/COVID-19-worldwide.xlsx')
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

                diedOneIn = 0
                if totalDeaths > 0:
                    diedOneIn = pop * 1000 / totalDeaths
                current['diedOneIn'] = diedOneIn

                infectedOneIn = 0
                if totalCases > 0:
                    infectedOneIn = pop * 1000 / totalCases
                current['infectedOneIn'] = infectedOneIn

                # store the last value for the map view.
                if index == len(self.data) - 1 or last != self.data[index + 1]['country']:
                    deathRate = current['newDeaths'] * 100 / (pop * 1000)
                    infectionRate = current['newCases'] * 100 / (pop * 1000)
                    self.mapView.append(
                        {'country': last, 'totalDeaths': totalDeaths, 'totalCases': totalCases,
                         'deathsPerPopulation': deathsPerPopulation,
                         'casesPerPopulation': casesPerPopulation,
                         'diedOneIn': diedOneIn, 'infectedOneIn': infectedOneIn,
                         'diedLastDay': current['newDeaths'], 'infectedLastDay': current['newCases'],
                         'deathRate': deathRate, 'infectionRate': infectionRate})
                index = index + 1

            else:
                self.data.__delitem__(index)

        def getPP(elem):
            return elem['deathsPerPopulation']

        self.mapView.sort(key=getPP, reverse=True)
        for i in range(0, len(self.mapView) - 1):
            self.orderedCountries.append(self.mapView[i]['country'])

    def getPopulation(self, last):
        if last in self.population:
            pop = int(self.population[last])
        else:
            print("Population of " + last + " is not found.")
            pop = 0
            # pop = current['population'] / 1000
        # print(last + " - UN Population:" + str(pop) + ", WB population:" + str(current['population'] / 1000))
        return pop

    def createPlots(self):
        fig = px.line(self.data, x='date', y='newDeaths', color='country', title="Number of deaths / date / country",
                      labels={"date": "Date", "newDeaths": "New Deaths", "country": "Country"},
                      category_orders={'country': self.orderedCountries},
                      color_discrete_sequence=px.colors.qualitative.Alphabet)
        fig.write_html("../Website/generated/daily-deaths.html")

        fig = px.line(self.data, x='date', y='dailyDeathsPerPopulation', color='country',
                      title="Deaths / popluation / date / country",
                      labels={"date": "Date", "newDeaths": "New Deaths", "country": "Country",
                              "dailyDeathsPerPopulation": "New deaths per population"},
                      category_orders={'country': self.orderedCountries},
                      color_discrete_sequence=px.colors.qualitative.Alphabet,
                      hover_data=["newDeaths"])
        fig.write_html("../Website/generated/daily-deaths-per-population.html")

        fig = px.line(self.data, x='date', y='totalDeaths', color='country', title="Total deaths per country",
                      labels={"date": "Date", "totalDeaths": "Total Deaths", "country": "Country"},
                      category_orders={'country': self.orderedCountries},
                      color_discrete_sequence=px.colors.qualitative.Alphabet)
        fig.write_html("../Website/generated/total-deaths.html")

        fig = px.line(self.data, x='date', y='deathsPerPopulation', color='country',
                      title="% of population died",
                      labels={"date": "Date", "deathsPerPopulation": "Population %",
                              "country": "Country", 'diedOneIn': 'One In ... people',
                              "totalDeaths": "Total"},
                      category_orders={'country': self.orderedCountries}, hover_data=['totalDeaths', 'diedOneIn'],
                      color_discrete_sequence=px.colors.qualitative.Alphabet)
        fig.write_html("../Website/generated/total-deaths-per-population.html")

        fig = px.line(self.data, x='date', y='dailyCasesPerPopulation', color='country',
                      title="New cases / popluation / date / country",
                      labels={"date": "Date", "newCases": "New Cases", "country": "Country",
                              "dailyCasesPerPopulation": "New cases per population"},
                      category_orders={'country': self.orderedCountries},
                      color_discrete_sequence=px.colors.qualitative.Alphabet,
                      hover_data=["newCases", "dailyCasesPerPopulation"])
        fig.write_html("../Website/generated/daily-cases-per-population.html")

    def drawOnMap(self):
        # temps, geyser, gray_r, burg
        fig = px.choropleth(self.mapView, locations="country", locationmode="country names",
                            color="deathsPerPopulation",
                            hover_data=["totalDeaths", "diedOneIn"], color_continuous_scale='temps',
                            projection='orthographic',
                            labels={"deathsPerPopulation": "Population %", "country": "Country",
                                    'diedOneIn': 'One In ... people',
                                    "totalDeaths": "Total"}, title="% of population died")
        fig.write_html("../Website/generated/deaths-per-population-total-map.html")

        fig = px.choropleth(self.mapView, locations="country", locationmode="country names", color="deathRate",
                            hover_data=["diedLastDay"], color_continuous_scale='temps',
                            projection='orthographic',
                            labels={"deathRate": "% of population died on the last day", "country": "Country",
                                    "diedLastDay": "Died on the last day"},
                            title="% of population died on the last day - Presumably correlated to infection rate 2-3 weeks ago")
        fig.write_html("../Website/generated/deaths-per-population-last-day-map.html")

        fig = px.choropleth(self.mapView, locations="country", locationmode="country names",
                            color="casesPerPopulation",
                            hover_data=["totalCases", "infectedOneIn"], color_continuous_scale='temps',
                            projection='orthographic',
                            labels={"casesPerPopulation": "Population %", "country": "Country",
                                    'infectedOneIn': 'One In ... people',
                                    "totalCases": "Total"}, title="% of population infected")
        fig.write_html("../Website/generated/cases-per-population-total-map.html")

        fig = px.choropleth(self.mapView, locations="country", locationmode="country names", color="infectionRate",
                            hover_data=["infectedLastDay"], color_continuous_scale='temps',
                            projection='orthographic',
                            labels={"infectionRate": "% of population infected on the last day", "country": "Country",
                                    "infectedLastDay": "Infected on the last day"},
                            title="% of population infected on the last day")
        fig.write_html("../Website/generated/cases-per-population-last-day-map.html")
        # print(self.mapView)


if __name__ == '__main__':
    plot = CoronaPlot()
    plot.createPlots()
    plot.drawOnMap()
