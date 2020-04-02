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