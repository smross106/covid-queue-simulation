"""
Sets up the Actor class, the simple agent that simulates human behaviour



Some parameters
15 steps per timestep, 2 timesteps per second
Each Actor moves randomly in a 5x5 pixel grid to keep the screen dynamic
"""

from random import random, choice, randint
import pygame
import app1

#This controls the chance of going to the shops at a given hour in the simulation (index 0 is chance of going out at 00:00)
#Intermediate values found by interpolation
#These values were chosen arbitrarily, to be replaced by some proper market research
shopTimeChance = [0,0,0,0,0,0,0.00152,0.00152,0.00693,0.00693,0.0134,0.0134,
0.0123,0.0123,0.0150,0.0150,0.0215,0.0215,0.00152,0.00152,0.0112,0.0112,0,0]


class Actor(object):
    #This actor acts on a whim to go to the shops and may or may not check the app before doing so
    def __init__(self, homeLocation,appMode):
        self.homeLocation = homeLocation
        self.shoppedToday = False
        self.appMode = appMode

        self.location = homeLocation

        #what shop am I trying to get to
        self.targetShops = None
        #what shop am I at
        self.shop = None

        self.mode = 0
        #0 - at home
        #1 - moving to shops
        #2 - at shops
        #3 - moving home

        self.key = {"shop":None, "slot":None}


    def run(self,time, Neighbourhood, appFunction):
        if time%24==0:
            self.shoppedToday = False
        
        if self.shoppedToday == False:
            self.goToShops(time,Neighbourhood,appFunction)

    def goToShops(self,time, neighbourhood, appFunction): 
        roll = random()
        odds = shopTimeChance[int(time%24)] * 1.403
        shop = choice(neighbourhood.shops)

        if roll<=odds:
            adjustedShop = appFunction[self.appMode](shop, neighbourhood)
            
            if type(adjustedShop)!=Shop:
                pass
            else:
                self.shoppedToday = True
                self.targetShops = shop
                self.mode = 1

    def draw(self,screen, tick):
        circleSize = 2


        if self.mode==0:
            #At home
            x = int(self.homeLocation[0] )
            y = int(self.homeLocation[1])

            if self.shoppedToday:
                pygame.draw.circle(screen,(0,127,0),(x,y),circleSize)
            else:
                pygame.draw.circle(screen,(255,0,0),(x,y),circleSize)
        
        if self.mode==1:
            #Moving to the shops from home
            newX = int((self.targetShops.location[0]-self.homeLocation[0])/10 * (tick+1)) + self.homeLocation[0]
            newY = int((self.targetShops.location[1]-self.homeLocation[1])/10 * (tick+1)) + self.homeLocation[1]
            if [newX,newY] == self.targetShops.location:
                self.shop = self.targetShops
                self.shop.queue.append(self)
                self.mode=2

            pygame.draw.circle(screen,(0,255,0),(newX,newY),circleSize)
        
        if self.mode==2:
            #At the shops
            pygame.draw.circle(screen,(0,0,255),self.shop.location,circleSize)
        
        if self.mode==3:
            #Moving home from the shops
            newX = int((self.shop.location[0]-self.homeLocation[0])/10 * (9-tick)) + self.homeLocation[0]
            newY = int((self.shop.location[1]-self.homeLocation[1])/10 * (9-tick)) + self.homeLocation[1]
            if [newX,newY] == self.homeLocation:
                self.shop = None
                self.mode = 0
        

            pygame.draw.circle(screen,(255,255,255),(newX,newY),circleSize)

    def shadowDraw(self):
        if self.mode==0:
            #At home
            pass
        
        if self.mode==1:
            #Move to target shop
            self.shop = self.targetShops
            self.shop.queue.append(self)
            self.mode = 2

        
        if self.mode==2:
            #At the shops
            pass
        
        if self.mode==3:
            self.shop = None
            self.mode = 0


class Actor2(object):
    #This Actor is smarter, they will set a preferred shop at the start of the day and 
    #then use the app to determine the best time to visit
    #They will also check if a shop queue is too long when they arrive and go somewhere else if it is

    def __init__(self,homeLocation,appMode):
        self.homeLocation = homeLocation

        self.previousLocation = homeLocation
        
        self.appMode = appMode

        self.shoppedToday = False
        self.preferredShop = None

        self.shopAt = None
        self.shopTarget = None

        self.mode = 0

        self.key = None
    
    def run(self,time,neighbourhood,appFunction):
        if int((time*6)%(24*6))==0:
            self.shoppedToday = False
            self.preferredShop = choice(neighbourhood.shops)
            self.key = appFunction[self.appMode-10](self.preferredShop,neighbourhood)
            
        
        if int((time*6)%(24*6))==int(self.key["slot"]*6) and self.shoppedToday==False and type(self.key["shop"])==Shop:
            self.mode = 1
            self.shopTarget = self.key["shop"]



    def draw(self,screen,tick):    
        circleSize = 2

        if self.mode==0:
            #At home
            if self.shoppedToday:
                pygame.draw.circle(screen,(0,127,0),self.homeLocation,circleSize)
            else:
                pygame.draw.circle(screen,(255,0,0),self.homeLocation,circleSize)
        
        if self.mode==1:
            #Moving to the shops from home
            newX = int((self.shopTarget.location[0]-self.previousLocation[0])/10 * (tick+1)) + self.previousLocation[0]
            newY = int((self.shopTarget.location[1]-self.previousLocation[1])/10 * (tick+1)) + self.previousLocation[1]
            if [newX,newY] == self.shopTarget.location:
                self.shopAt = self.shopTarget
                self.shopAt.queue.append(self)
                self.mode=2
                self.shoppedToday = True

            pygame.draw.circle(screen,(0,255,0),(newX,newY),circleSize)
        
        if self.mode==2:
            #At the shops
            pygame.draw.circle(screen,(0,0,255),self.shopAt.location,circleSize)
        
        if self.mode==3:
            #Moving home from the shops
            newX = int((self.homeLocation[0]-self.previousLocation[0])/10 * (tick+1)) + self.previousLocation[0]
            newY = int((self.homeLocation[1]-self.previousLocation[1])/10 * (9-tick+1)) + self.previousLocation[1]
            if [newX,newY] == self.homeLocation:
                self.shopAt = None
                self.mode = 0
        
            pygame.draw.circle(screen,(255,255,255),(newX,newY),circleSize)
    
    def shadowDraw(self):    

        if self.mode==0:
            #At home
            self.previousLocation = self.homeLocation
        
        if self.mode==1:
            #Moving to the shops from home
            self.shopAt = self.shopTarget
            self.shopAt.queue.append(self)
            self.mode=2
            self.shoppedToday = True
            self.previousLocation = self.shopAt.location
        
        if self.mode==2:
            #At the shops
            pass
        
        if self.mode==3:
            #Moving home from the shops
            self.shopAt = None
            self.mode = 0
        

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

        self.slots = [0]*24*6

        self.smartSlots = [0]*24*6

    def __lt__(self,other):
        return(self)
    
    def __eq__(self,other):
        return(self)
    
    def __gt__(self,other):
        return(self)
    
    def run(self, time, tick):

        self.historicQueue.append(len(self.queue))

        if time%24==0:
            for i in range(0,len(self.slots)):
                self.slots[i] = self.throughput
            if len(self.historicQueue)>24*6:
                offset = len(self.historicQueue)-(24*6)
                for i in range(0,len(self.smartSlots)):
                    self.smartSlots[i] = self.throughput-self.historicQueue[offset+i]
    
        if len(self.queue)==0:
            pass
        else:
            if self.throughput<len(self.queue):
                processed = self.throughput
            else:
                processed = len(self.queue)
            
            for i in range(0,processed):
                self.queue[0].targetShops=None
                self.queue[0].mode = 3
                self.queue.remove(self.queue[0])
        
    def draw(self,screen):
        width = 20
        height = 2*self.throughput

        barheight = 2*len(self.queue)

       

        pygame.draw.rect(screen,(0,255,0),(self.location[0]-int(width/2),self.location[1],width,barheight))
        pygame.draw.rect(screen,(0,0,255),(self.location[0]-int(width/2),self.location[1],width,height),2)



