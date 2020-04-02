import csv
from actor import Shop, Neighbourhood, Actor
from random import randint, choice

def setup(gridWidth,nShops):
    gridSize = 8
    gridOffset = 50
    #gridWidth = 50
    #nShops = int(gridWidth**2 / 100)
    #TOTALLY ARBITRARY DECISION of 100 people shopping per day per shop
    shops = []
    for i in range(0,nShops):
        shops.append(Shop([(gridSize*randint(0,gridWidth))+gridOffset,(gridSize*randint(0,gridWidth))+gridOffset],10))
    hood = Neighbourhood(shops)
    shopLocations = [i.location for i in hood.shops]
    actors = []

    strategies = [2,0]

    for i in range(0,gridWidth):
        for j in range(0,gridWidth):
            if not ([(gridSize*i)+gridOffset,(gridSize*j)+gridOffset] in shopLocations):
                new = Actor([(gridSize*i)+gridOffset,(gridSize*j)+gridOffset],choice(strategies))
                actors.append(new)
    
    return(actors,hood)

def writeDataToCSV(data,filename):
    with open(filename+".csv","w",newline="") as csvfile:
        datawriter = csv.writer(csvfile,delimiter=",",
        quotechar="|",quoting=csv.QUOTE_MINIMAL)
        datawriter.writerows(data)