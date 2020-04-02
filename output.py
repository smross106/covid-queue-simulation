from actor import Actor, Neighbourhood, Shop
from app0 import *
from random import randint
import helper
import matplotlib.pyplot as plt
from numpy import mean,zeros
import time

start = time.time()

tick = 0
hour = 0
endTick = 6*10*24


size = 8
actors,hood = helper.setup(64*size,5*(size**2))

timedata = []

while tick<endTick:
    #Update all actor states every 10 ticks
    if tick%10==0:
        print("\t",str(int(hour))+":"+str(int(hour%1 * 60)))
        for i in actors:
            i.run(hour,hood,[blind,block,another])
        
        for shop in hood.shops:
            shop.run(hour)

        timedata.append(tick)
    
    for i in actors:
        i.shadowDraw(tick%10)

    tick += 10
    hour = (tick/60)%24
    if tick>6*10*24:
        running = False

fed = 0
for i in actors:
    if i.shoppedToday:fed+=1

nMean = 10

newTimeData = []
for i in timedata:
    newTimeData.append(i/60)

sumQueueData = []
for i in range(len(hood.shops[0].historicQueue)):sumQueueData.append(0)
for i in range(0,nMean):
    for j in range(len(hood.shops[i].historicQueue)):
        sumQueueData[j]+=hood.shops[i].historicQueue[j]
meanQueueData = []
for j in sumQueueData:
    meanQueueData.append(j/nMean)


print(fed/len(actors))

print(time.time()-start)

for i in range(0,nMean):
    plt.plot(newTimeData,hood.shops[i].historicQueue,linewidth=0.25)

plt.plot(newTimeData,meanQueueData,linewidth=3)

plt.plot([0,24],[10,10],color="red")
plt.title("50% 'another', 50% 'blind' technique, "+str(int(100*fed/len(actors)))+"% of people fed")
plt.xlim([0,24])
plt.ylim(0)

plt.show()