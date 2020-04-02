import pygame
from pygame.locals import *
from actor import Actor, Neighbourhood, Shop
from app0 import *
from random import randint

pygame.init()
screen = pygame.display.set_mode([1400,800])
clock = pygame.time.Clock()

tick = 0
hour = 0

running = True

def setup():
    gridSize = 8
    gridOffset = 50
    gridWidth = 50
    nShops = 4
    shops = []
    for i in range(0,nShops):
        shops.append(Shop([(gridSize*randint(0,gridWidth))+gridOffset,(gridSize*randint(0,gridWidth))+gridOffset],5))
    hood = Neighbourhood(shops)
    shopLocations = [i.location for i in hood.shops]
    actors = []
    for i in range(0,gridWidth):
        for j in range(0,gridWidth):
            if not ([(gridSize*i)+gridOffset,(gridSize*j)+gridOffset] in shopLocations):
                new = Actor([(gridSize*i)+gridOffset,(gridSize*j)+gridOffset],randint(0,1))
                actors.append(new)
    
    return(actors,hood)

def graph(screen,x,y,xScale,yScale,data,limit):

    if len(data)==0:
        pygame.draw.line(screen,(255,255,255),(x,y),(x,y - (yScale*20)))
    elif max(data)<20:
        pygame.draw.line(screen,(255,255,255),(x,y),(x,y - (yScale*20)))
    else:
        pygame.draw.line(screen,(255,255,255),(x,y),(x,y - (yScale*max(data))))

    pygame.draw.line(screen,(255,255,255),(x,y),(x+(24*6*xScale),y))

    pygame.draw.line(screen,(255,0,0),(x,y-(yScale*limit)),(x+(24*6*xScale),y-(yScale*limit)))

    for i in range(0,len(data)-1):
        point =data[i]
        nextPoint = data[i+1]
        col = (0,255,0)
        pygame.draw.line(screen,col,(x+int(i*xScale),y-int(point*yScale)),(x+int((i+1)*xScale),y-int(nextPoint*yScale)),1)


actors,hood = setup()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.fill((0,0,0))


    #Update all actor states every 10 ticks
    if tick%10==0:
        print("\t",hour)
        for i in actors:
            i.run(hour,hood,[blind,block])
        
        for shop in hood.shops:
            shop.run(hour)

    #Draw all actors
    for i in actors:
        i.draw(screen,tick%10)

    #Draw graph
    for i in range(0,2):
        xScale = 5/3.
        yScale = 5
        graph(screen,800,200+(25*yScale + 100)*i,xScale,yScale,hood.shops[i].historicQueue,hood.shops[i].throughput)
    for i in range(0,2):
        xScale = 5/3.
        yScale = 5
        graph(screen,1100,200+(25*yScale + 100)*i,xScale,yScale,hood.shops[i+2].historicQueue,hood.shops[i+2].throughput)
    """
    xScale = 5/3.
    yScale = 5
    pygame.draw.line(screen,(255,255,255),(100,400),(100,300))
    pygame.draw.line(screen,(255,255,255),(100,400),(340,400))
    pygame.draw.line(screen,(255,0,0),(100,400-(yScale*hood.shops[0].throughput)),(340,400-(yScale*hood.shops[0].throughput)))
    for i in range(0,len(hood.shops[0].historicQueue)-1):
        point = hood.shops[0].historicQueue[i]
        nextPoint = hood.shops[0].historicQueue[i+1]
        col = (0,255,0)
        pygame.draw.line(screen,col,(100+int(i*xScale),400-int(point*yScale)),(100+int((i+1)*xScale),400-int(nextPoint*yScale)),1)
    """

    pygame.display.update()
    clock.tick(60)
    tick += 1
    hour = (tick/60)%24
