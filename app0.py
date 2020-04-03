from random import choice

def blind(shop,neighbourhood):
    #Go to the intended shop
    return(shop)

def block(shop,neighbourhood):
    #If there is a significant queue (will not be cleared in next 10 minutes) do not go to shop
    queue = len(shop.queue)
    if queue>shop.throughput:
        return(None)
    else:
        return(shop)

def another(shop, neighbourhood):
    #If there is a significant queue (will not be cleared in next 10 minutes) try another random shop
    #If there is a queue there do not go to shop
    queue = len(shop.queue)
    if queue<shop.throughput:
        return(shop)
    else:
        newShop = choice(neighbourhood.shops)
        if len(newShop.queue)>newShop.throughput:
            return(None)
        else:
            return(newShop)

def quietest(shop,neighbourhood):
    if len(shop.queue)<shop.throughput:
        return(shop)
    else:
        queues = []
        for i in neighbourhood.shops:
            queues.append([len(i.queue),i])
        return(sorted(queues)[0][1])

def oneofquietest(shop,neighbourhood):
    if len(shop.queue)<shop.throughput:
        return(shop)
    else:
        queues = []
        for i in neighbourhood.shops:
            queues.append([len(i.queue),i])
        tenpercent = int(len(queues)/10)
        return(choice(sorted(queues)[0:tenpercent])[1])
