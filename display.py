import pygame
from pygame.locals import *
from actor import Actor, Neighbourhood, Shop
from app0 import *
from random import randint
import helper
from math import sin, cos, pi, radians

pygame.init()
screen = pygame.display.set_mode([1400,800])
clock = pygame.time.Clock()

tick = 0
hour = 0

running = True



def graph(screen,x,y,xScale,yScale,data,limit):

    cols = [(255,0,0),(0,255,0),(0,0,255),(255,0,255)]

    if len(data[0])==0:
        pygame.draw.line(screen,(255,255,255),(x,y),(x,y - (yScale*20)))
    elif max(data[0])<20:
        pygame.draw.line(screen,(255,255,255),(x,y),(x,y - (yScale*20)))
    else:
        pygame.draw.line(screen,(255,255,255),(x,y),(x,y - (yScale*max(data[0]))))

    pygame.draw.line(screen,(255,255,255),(x,y),(x+(24*6*xScale),y))

    pygame.draw.line(screen,(255,0,0),(x,y-(yScale*limit)),(x+(24*6*xScale),y-(yScale*limit)))

    for j in range(0,len(data)):
        for i in range(0,len(data[j])-1):
            point =data[j][i]
            nextPoint = data[j][i+1]
            col = (0,255,0)
            pygame.draw.line(screen,cols[j],(x+int(i*xScale),y-int(point*yScale)),(x+int((i+1)*xScale),y-int(nextPoint*yScale)),1)


actors,hood = helper.setup(64)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    screen.fill((0,0,0))


    #Update all actor states every 10 ticks
    if tick%10==0:
        print("\t",str(int(hour))+":"+str(int(hour%1 * 60))+"\t"+str(tick))
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
    alldata = []
    for i in hood.shops: alldata.append(i.historicQueue)

    xScale = 5/3.
    yScale = 5
    graph(screen,800,800,xScale,yScale,alldata,hood.shops[0].throughput)

    #Draw clock
    centre = [750,100]
    pygame.draw.circle(screen,(255,255,255),centre,40,2)
    theta = radians(tick/2)
    #hour hand
    length = 20
    endX = centre[0] + (length * sin(theta))
    endY = centre[1] - (length * cos(theta))
    pygame.draw.line(screen,(255,255,255),centre,[endX,endY],3)
    #minute hand
    phi = radians(tick*6)
    length2 = 30
    endX = centre[0] + (length2 * sin(phi))
    endY = centre[1] - (length2 * cos(phi))
    pygame.draw.line(screen,(255,255,255),centre,[endX,endY],1)

    """
    for i in range(0,2):
        xScale = 5/3.
        yScale = 5
        graph(screen,1100,200+(25*yScale + 100)*i,xScale,yScale,hood.shops[i+2].historicQueue,hood.shops[i+2].throughput)
"""

    pygame.display.update()
    clock.tick(30)
    tick += 1
    hour = (tick/60)%24
