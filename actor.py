"""
Sets up the Actor class, the simple agent that simulates human behaviour



Some parameters
15 steps per timestep, 2 timesteps per second
Each Actor moves randomly in a 5x5 pixel grid to keep the screen dynamic
"""

from random import random, choice, randint
import pygame

#This controls the chance of going to the shops at a given hour in the simulation (index 0 is chance of going out at 00:00)
#Intermediate values found by interpolation
#These values were chosen arbitrarily, to be replaced by some proper market research
shopTimeChance = [0,0,0,0,0,0,0.05,0.1,0.2,0.15,0.15,0.15,0.15,0.2,0.4,0.5,0.3,0.3,0.4,0.4,0.3,0.2,0.1,0.05,0]


class Actor(object):
    def __init__(self, homeLocation,appMode):
        self.homeLocation = homeLocation
        self.shoppedToday = False
        self.appMode = appMode

        self.location = homeLocation

        self.targetShops = None
        self.shop = None


    def run(self,time, Neighbourhood, appFunction):
        #if time%24==0:
        #    self.shoppedToday = False
        
        if self.shoppedToday == False and self.shop == None:
            self.goToShops(time,Neighbourhood.shops,appFunction)

    def goToShops(self,time, shopList, appFunction): 
        roll = random()
        odds = shopTimeChance[int(time%24)] / 12
        shop = choice(shopList)

        if roll<=odds:
            adjustedShop = appFunction[self.appMode](shop)
            if adjustedShop==None:
                pass
            else:
                self.shoppedToday = True
                self.targetShops = shop
            
    
    def draw(self,screen, tick):
        circleSize = 2


        if self.shop == None and self.targetShops == None:
            #At home
            x = int(self.homeLocation[0] )
            y = int(self.homeLocation[1])

            if self.shoppedToday:
                pygame.draw.circle(screen,(0,127,0),(x,y),circleSize)
            else:
                pygame.draw.circle(screen,(255,0,0),(x,y),circleSize)
        
        if self.targetShops!=None and self.shop==None:
            #Moving to the shops from home
            newX = int((self.targetShops.location[0]-self.homeLocation[0])/10 * (tick+1)) + self.homeLocation[0]
            newY = int((self.targetShops.location[1]-self.homeLocation[1])/10 * (tick+1)) + self.homeLocation[1]
            if [newX,newY] == self.targetShops.location:
                self.shop = self.targetShops
                self.shop.queue.append(self)

            pygame.draw.circle(screen,(0,255,0),(newX,newY),circleSize)
        
        if self.shop!=None and self.targetShops==self.shop:
            #At the shops
            pygame.draw.circle(screen,(0,0,255),self.shop.location,circleSize)
        
        if self.shop!=None and self.targetShops==None:
            #Moving home from the shops
            newX = int((self.shop.location[0]-self.homeLocation[0])/10 * (9-tick)) + self.homeLocation[0]
            newY = int((self.shop.location[1]-self.homeLocation[1])/10 * (9-tick)) + self.homeLocation[1]
            if [newX,newY] == self.homeLocation:
                self.shop = None
        

            pygame.draw.circle(screen,(255,255,255),(newX,newY),circleSize)

    def shadowDraw(self,tick):


        if self.shop == None and self.targetShops == None:
            #At home
            pass
        
        if self.targetShops!=None and self.shop==None:
            self.shop = self.targetShops
            self.shop.queue.append(self)

        
        if self.shop!=None and self.targetShops==self.shop:
            #At the shops
            pass
        
        if self.shop!=None and self.targetShops==None:
            self.shop = None


            


class Neighbourhood(object):
    def __init__(self,shops):
        self.shops = shops

class Shop(object):
    def __init__(self, location, throughput):
        self.location = location
        self.throughput = throughput
        #Number of people that can be served per tick

        self.queue = []

        self.historicQueue = []
    
    def run(self, time):

        self.historicQueue.append(len(self.queue))

        #if time%24==0:
        #    self.historicQueue=[]
        if len(self.queue)==0:
            pass
        else:
            if self.throughput<len(self.queue):
                processed = self.throughput
            else:
                processed = len(self.queue)
            
            for i in range(0,processed):
                self.queue[0].targetShops=None
                self.queue.remove(self.queue[0])
        
        

