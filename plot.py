import plotly.express as px
import json

from Generator import world, germany


class CoronaPlot:
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
                      category_orders={'country': self.orderedCountries}, hover_data=['totalDeaths'],
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
        # print(self.mapView)
        # temps, geyser, gray_r, burg
        fig = px.choropleth(self.mapView, geojson=self.worldGeo, locations="region", locationmode="geojson-id",
                            color="deathsPerPopulation", hover_data=["totalDeaths", "diedOneIn"],
                            color_continuous_scale='temps', projection='orthographic',
                            labels={"deathsPerPopulation": "Population %", "country": "Country",
                                    'diedOneIn': 'One In ... people',
                                    "totalDeaths": "Total"}, title="% of population died")
        fig.write_html("../Website/generated/deaths-per-population-total-map.html")

        fig = px.choropleth(self.mapView, locations="region", locationmode="country names", color="deathRate",
                            hover_data=["diedLastDay"], color_continuous_scale='temps',
                            projection='orthographic',
                            labels={"deathRate": "% of population died on the last day", "country": "Country",
                                    "diedLastDay": "Died on the last day"},
                            title="% of population died on the last day - Presumably correlated to infection rate 2-3 weeks ago")
        fig.write_html("../Website/generated/deaths-per-population-last-day-map.html")

        fig = px.choropleth(self.mapView, locations="region", locationmode="country names",
                            color="casesPerPopulation",
                            hover_data=["totalCases", "infectedOneIn"], color_continuous_scale='temps',
                            projection='orthographic',
                            labels={"casesPerPopulation": "Population %", "country": "Country",
                                    'infectedOneIn': 'One In ... people',
                                    "totalCases": "Total"}, title="% of population infected")
        fig.write_html("../Website/generated/cases-per-population-total-map.html")

        fig = px.choropleth(self.mapView, locations="region", locationmode="country names", color="infectionRate",
                            hover_data=["infectedLastDay"], color_continuous_scale='temps',
                            projection='orthographic',
                            labels={"infectionRate": "% of population infected on the last day", "country": "Country",
                                    "infectedLastDay": "Infected on the last day"},
                            title="% of population infected on the last day")
        fig.write_html("../Website/generated/cases-per-population-last-day-map.html")

    def loadWorld(self):
        with open('data/countries.geojson') as json_file:
            self.worldGeo = json.load(json_file)

        for object in self.worldGeo["features"]:
            x = object["properties"]["name"]
            if x != "Germany":
                object["id"] = x.upper()


if __name__ == '__main__':
    plot = CoronaPlot()
    plot.loadWorld()

    plot.data, plot.mapView, plot.orderedCountries = world.loadCoronaData()

    germanyView, germanyGeo = germany.loadCoronaData()

    for node in germanyGeo["features"]:
        plot.worldGeo["features"].append(node)

    for row in germanyView:
        plot.mapView.append(row)

    # plot.createPlots()
    plot.drawOnMap()
