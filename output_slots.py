from actor import Actor, Actor2, Neighbourhood, Shop
from app0 import *
from app1 import *
from random import randint
import helper
import matplotlib.pyplot as plt
from numpy import mean,zeros
import time

start = time.time()

nDays = 4

tick = 0
hour = 0
endTick = 6*10*24 * nDays

def roundMean(x):
    return("{:.2f}".format((int(mean(x)*10)/10.)))

size = 2
actors,hood = helper.setup2(64*size,10)

timedata = []

while tick<endTick:
    #Update all actor states every 10 ticks
    if tick%10==0:
        print("\t",str(int(hour))+":"+str(int(hour%1 * 60)))
        for shop in hood.shops:
            shop.run(hour,tick)


        for i in actors:
            if type(i)==Actor:
                i.run(hour,hood,[blind])
            elif type(i)==Actor2:
                i.run(hour,hood,[randomSlotPref,randomSlotRandom,slotsPerShop,slotsFromBusyYesterday])
        
        
        timedata.append(tick)
    
    for i in actors:
        i.shadowDraw()

    tick += 10
    hour = (tick/60)%24

    if tick%(24*60)==0:
        fed = 0
        noSlot = 0
        for i in actors:
            if i.shoppedToday:fed+=1
            if i.key["shop"]==None:noSlot+=1

        print(fed/len(actors))
        print(noSlot/len(actors))

        print(hood.shops[0].slots)
    


print(time.time()-start)

GRAPHMODE = 0
meanQueueData = []
nMean = int(len(hood.shops)/3)
newTimeData = []
plotdata = []
for i in timedata:
    newTimeData.append(i/60)

if GRAPHMODE==0:
    
    sumQueueData = []

    daylength = len(hood.shops[0].historicQueue)

    for i in range(len(timedata)):sumQueueData.append(0)

    for i in range(nMean):
        print(len(hood.shops[i].historicQueue),len(timedata))
        for j in range(daylength):
                sumQueueData[j]+=hood.shops[i].historicQueue[j]
        plotdata.append(hood.shops[i].historicQueue)

    
    for j in sumQueueData:
        meanQueueData.append(j/nMean)

if nMean>20:
    nMean = 20

for i in range(0,nMean):
    plt.plot(newTimeData,plotdata[i],linewidth=0.25)

plt.plot(newTimeData,meanQueueData,linewidth=3)


if GRAPHMODE==0:
    plt.plot([0,24*nDays],[10,10],color="red")
    plt.xlim([0,24*nDays])

plt.title("100% 'random_slot_at_preference' technique \n "+str(int(100*fed/len(actors)))+"% of people fed \n Day 1 average queue length: "+roundMean(meanQueueData[0:144])+"\n Subsequent days average queue length: "+roundMean(meanQueueData[144:]))

plt.ylim(0)

plt.show()