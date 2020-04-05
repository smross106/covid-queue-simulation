import pygame
from pygame.locals import *
from actor import Actor, Neighbourhood, Shop
from app0 import *
from random import randint
import helper

pygame.init()
screen = pygame.display.set_mode([1400,800])
clock = pygame.time.Clock()

tick = 0
hour = 0

running = True



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


actors,hood = helper.setup(64,5)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.fill((0,0,0))


    #Update all actor states every 10 ticks
    if tick%10==0:
        print("\t",str(int(hour))+":"+str(int(hour%1 * 60)))
        for i in actors:
            i.run(hour,hood,[blind,block])
        
        for shop in hood.shops:
            shop.run(hour,tick)

    #Draw all actors
    for i in actors:
        i.draw(screen,tick%10)
    for i in hood.shops:
        i.draw(screen)

    #Draw graph
    for i in range(0,1):
        xScale = 5/3.
        yScale = 5
        graph(screen,800,200+(25*yScale + 100)*i,xScale,yScale,hood.shops[i].historicQueue,hood.shops[i].throughput)
    """
    for i in range(0,2):
        xScale = 5/3.
        yScale = 5
        graph(screen,1100,200+(25*yScale + 100)*i,xScale,yScale,hood.shops[i+2].historicQueue,hood.shops[i+2].throughput)
"""

    pygame.display.update()
    clock.tick(60)
    tick += 1
    hour = (tick/60)%24
