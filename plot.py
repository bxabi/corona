import json
import os
import sys

import plotly.express as px
import time

from Regions.brazil import Brazil
from Regions.china import China
from Regions.germany import Germany
from Regions.italy import Italy
from Regions.russia import Russia
from Regions.usa import USA
from Regions.world import World

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")


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

        fig = px.line(self.data, x='date', y='casesPerPopulation', color='country',
                      title="% of population infected",
                      labels={"date": "Date", "casesPerPopulation": "Population %",
                              "country": "Country", 'infectedOneIn': 'One In ... people',
                              "totalCases": "Total"},
                      category_orders={'country': self.orderedCountries}, hover_data=['totalCases'],
                      color_discrete_sequence=px.colors.qualitative.Alphabet)
        fig.write_html("../Website/generated/total-cases-per-population.html")

    def drawOnMap(self):
        # temps, geyser, gray_r, burg
        fig = px.choropleth(self.mapView,
                            geojson=self.worldGeo, locationmode="geojson-id",
                            # locationmode="country names",
                            locations="region",
                            color="deathsPerPopulation", hover_data=["totalDeaths", "diedOneIn"],
                            color_continuous_scale='temps', projection='hammer',
                            labels={"deathsPerPopulation": "Population %", "country": "Country",
                                    'diedOneIn': 'One In ... people',
                                    "totalDeaths": "Total"}, title="% of population died")
        fig.write_html("../Website/generated/deaths-per-population-total-map.html")

        fig = px.choropleth(self.mapView,
                            geojson=self.worldGeo, locationmode="geojson-id",
                            # locationmode="country names",
                            locations="region", color="deathRate", hover_data=["diedLastDay"],
                            color_continuous_scale='temps', projection='hammer',
                            labels={"deathRate": "% of population died on the last day", "country": "Country",
                                    "diedLastDay": "Died on the last day"},
                            title="% of population died on the last day - Presumably correlated to infection rate 2-3 weeks ago")
        fig.write_html("../Website/generated/deaths-per-population-last-day-map.html")

        fig = px.choropleth(self.mapView, locations="region",
                            # locationmode="country names",
                            geojson=self.worldGeo, locationmode="geojson-id",
                            color="casesPerPopulation",
                            hover_data=["totalCases", "infectedOneIn"], color_continuous_scale='temps',
                            projection='hammer',
                            labels={"casesPerPopulation": "Population %", "country": "Country",
                                    'infectedOneIn': 'One In ... people',
                                    "totalCases": "Total"}, title="% of population infected")
        fig.write_html("../Website/generated/cases-per-population-total-map.html")

        fig = px.choropleth(self.mapView,
                            geojson=self.worldGeo, locationmode="geojson-id",
                            # locationmode="country names",
                            locations="region", color="infectionRate",
                            hover_data=["infectedLastDay"], color_continuous_scale='temps',
                            projection='hammer',
                            labels={"infectionRate": "% of population infected on the last day", "country": "Country",
                                    "infectedLastDay": "Infected on the last day"},
                            title="% of population infected on the last day")
        fig.write_html("../Website/generated/cases-per-population-last-day-map.html")

    def loadWorld(self):
        with open('data/countries.geojson') as json_file:
            self.worldGeo = json.load(json_file)

        for object in self.worldGeo["features"]:
            x = object["properties"]["name"]
            if x != "Germany" and x != "United States of America" and x != "China" and x != "Russia" and x != "Italy" and x != "Brazil":
                object["id"] = x.upper()

    # to test different projections.
    # def testTheProjections(self):
    #     list = ['equirectangular',
    #             'mercator',
    #             'orthographic',
    #             'natural earth',
    #             'kavrayskiy7',
    #             'miller',
    #             'robinson',
    #             'eckert4',
    #             'azimuthal equal area',
    #             'azimuthal equidistant',
    #             'conic equal area',
    #             'conic conformal',
    #             'conic equidistant',
    #             'gnomonic',
    #             'stereographic',
    #             'mollweide',
    #             'hammer',
    #             'transverse mercator']
    #     for proj in list:
    #         fig = px.choropleth(self.mapView,
    #                             geojson=self.worldGeo, locationmode="geojson-id",
    #                             # locationmode="country names",
    #                             locations="region",
    #                             color="deathsPerPopulation", hover_data=["totalDeaths", "diedOneIn"],
    #                             color_continuous_scale='temps', projection=proj,
    #                             labels={"deathsPerPopulation": "Population %", "country": "Country",
    #                                     'diedOneIn': 'One In ... people',
    #                                     "totalDeaths": "Total"}, title=proj + " | % of population died")
    #         fig.show()


def simplify(node):
    c = node["geometry"]["coordinates"][0]
    i = len(c) - 2
    count = 0
    while i > 0:
        del c[i]
        i = i - 1
        count = count + 1
        if count == 2:  # keep every x'th element
            i = i - 1
            count = 0


def addToMap(view, geo, doSimplification=True):
    global node, row
    for node in geo["features"]:
        if doSimplification:
            simplify(node)
        plot.worldGeo["features"].append(node)
    for row in view:
        plot.mapView.append(row)


def getPP(elem):
    return elem['deathsPerPopulation']


if __name__ == '__main__':
    tt = time.time()

    plot = CoronaPlot()
    plot.loadWorld()

    start_time = time.time()
    world = World()
    plot.data = world.data
    plot.mapView = world.mapView
    print("World: " + str(time.time() - start_time) + " seconds.")

    start_time = time.time()
    germany = Germany()
    addToMap(germany.mapView, germany.geo, False)
    plot.data.extend(germany.plotData)
    print("Germany: " + str(time.time() - start_time) + " seconds.")

    start_time = time.time()
    usa = USA()
    addToMap(usa.mapView, usa.geo)
    print("USA: " + str(time.time() - start_time) + " seconds.")

    start_time = time.time()
    china = China()
    addToMap(china.mapView, china.geo)
    print("China: " + str(time.time() - start_time) + " seconds.")

    start_time = time.time()
    russia = Russia()
    addToMap(russia.mapView, russia.geo)
    print("Russia: " + str(time.time() - start_time) + " seconds.")

    start_time = time.time()
    italy = Italy()
    addToMap(italy.mapView, italy.geo, False)
    print("Italy: " + str(time.time() - start_time) + " seconds.")

    start_time = time.time()
    brazil = Brazil()
    addToMap(brazil.mapView, brazil.geo, False)
    plot.data.extend(brazil.plotData)
    print("Brazil: " + str(time.time() - start_time) + " seconds.")

    plot.orderedCountries = []
    plot.mapView.sort(key=getPP, reverse=True)
    for i in range(0, len(plot.mapView) - 1):
        plot.orderedCountries.append(plot.mapView[i]['region'])

    start_time = time.time()
    plot.createPlots()
    print("Plots: " + str(time.time() - start_time) + " seconds.")

    start_time = time.time()
    plot.drawOnMap()
    print("Maps: " + str(time.time() - start_time) + " seconds.")

    # plot.testTheProjections()
    print("Total Time: %s seconds" % (time.time() - tt))
