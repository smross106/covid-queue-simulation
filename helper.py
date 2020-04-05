import csv
from actor import Shop, Neighbourhood, Actor, Actor2
from random import randint, choice

def setup(gridWidth):
    gridSize = 8
    gridOffset = 50

    #Data supports the theory of ~1000 people per shop per day
    nShops = int((gridWidth**2) / 1000)

    shops = []
    XSpacing = int(gridSize*gridWidth/nShops)
    for i in range(0,nShops):
        shops.append(Shop([(XSpacing*i)+gridOffset,(gridSize*gridWidth)+int(gridOffset*1.5)],10))
    hood = Neighbourhood(shops)
    shopLocations = [i.location for i in hood.shops]
    actors = []

    strategies = [0,0]

    for i in range(0,gridWidth):
        for j in range(0,gridWidth):
            if not ([(gridSize*i)+gridOffset,(gridSize*j)+gridOffset] in shopLocations):
                new = Actor([(gridSize*i)+gridOffset,(gridSize*j)+gridOffset],choice(strategies))
                actors.append(new)
    
    return(actors,hood)

def setup2(gridWidth,percentSmart):
    gridSize = 8
    gridOffset = 50

    #Data supports the theory of ~1000 people per shop per day
    nShops = int((gridWidth**2) / 1000)

    shops = []
    XSpacing = int(gridSize*gridWidth/nShops)
    for i in range(0,nShops):
        new = Shop([(XSpacing*i)+gridOffset,(gridSize*gridWidth)+int(gridOffset*1.5)],10)
        shops.append(new)
    hood = Neighbourhood(shops)
    shopLocations = [i.location for i in hood.shops]
    actors = []

    actor1strategies = [1]
    actor2strategies = [13]

    for i in range(0,gridWidth):
        for j in range(0,gridWidth):
            if not ([(gridSize*i)+gridOffset,(gridSize*j)+gridOffset] in shopLocations):
                if randint(1,100)<=percentSmart:
                    new = Actor2([(gridSize*i)+gridOffset,(gridSize*j)+gridOffset],choice(actor2strategies))
                else:
                    new = Actor([(gridSize*i)+gridOffset,(gridSize*j)+gridOffset],choice(actor1strategies))
                actors.append(new)
    
    return(actors,hood)

def writeDataToCSV(data,filename):
    with open(filename+".csv","w",newline="") as csvfile:
        datawriter = csv.writer(csvfile,delimiter=",",
        quotechar="|",quoting=csv.QUOTE_MINIMAL)
        datawriter.writerows(data)