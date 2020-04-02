import pygame
from pygame.locals import *
from actor import Actor, Neighbourhood, Shop
from app0 import blind

pygame.init()
screen = pygame.display.set_mode([500,500])
clock = pygame.time.Clock()

tick = 0
hour = 0

running = True

def setup():
    actors = []
    for i in range(0,20):
        for j in range(0,20):
            if i!=5 or j!=5:
                new = Actor([(5*i)+20,(5*j)+20])
                actors.append(new)
    tesco = Shop([45,45],5)
    hood = Neighbourhood([tesco])
    return(actors,hood)

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
            i.run(hour,hood,blind)
        
        for shop in hood.shops:
            shop.run(hour)

    #Draw all actors
    for i in actors:
        i.draw(screen,tick%10)

    #Draw graph
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

    pygame.display.update()
    clock.tick(60)
    tick += 1
    hour = (tick/60)%24
