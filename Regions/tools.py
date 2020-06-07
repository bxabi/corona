def getMapviewRow(region, newCases, newDeaths, totalCases, totalDeaths, population):
    deathsPerPopulation = totalDeaths * 100 / population
    casesPerPopulation = totalCases * 100 / population

    diedOneIn = 0
    if totalDeaths > 0:
        diedOneIn = population / totalDeaths

    infectedOneIn = 0
    if totalCases > 0:
        infectedOneIn = population / totalCases

    deathRate = newDeaths * 100 / population
    infectionRate = newCases * 100 / population

    return {'region': region, 'totalDeaths': totalDeaths, 'totalCases': totalCases,
            'deathsPerPopulation': deathsPerPopulation,
            'casesPerPopulation': casesPerPopulation,
            'diedOneIn': diedOneIn, 'infectedOneIn': infectedOneIn,
            'diedLastDay': newDeaths, 'infectedLastDay': newCases,
            'deathRate': deathRate, 'infectionRate': infectionRate}
