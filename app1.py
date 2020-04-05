from random import randint,choice

#Standard advanced slot protocol:
#key = {
# "shop":shop,
# "slot":time code (hour)}

OPENING_TIME = 6
CLOSING_TIME = 21

#The following are for assigning slots to Actors
def randomSlotPref(preferredShop,neighbourhood):
    time = randint(OPENING_TIME,CLOSING_TIME) + (randint(0,5)/6.)
    key = {"shop":preferredShop,"slot":time}
    return(key)

def randomSlotRandom(preferredShop,neighbourhood):
    time = randint(OPENING_TIME,CLOSING_TIME) + (randint(0,5)/6.)
    shop = choice(neighbourhood.shops)
    key = {"shop":shop,"slot":time}
    return(key)

def slotsPerShop(preferredShop,neighbourhood):
    time = randint(OPENING_TIME,CLOSING_TIME) + (randint(0,5)/6.)
    shop = choice(neighbourhood.shops)
    
    if shop.slots[int(time*6)]==0:
        #return(slotsPerShop(preferredShop,neighbourhood))
        key =  {"shop":preferredShop,"slot":time}
        return(key)
    else:
        shop.slots[int(time*6)]-=1
        key =  {"shop":shop,"slot":time}
        return(key)

def slotsFromBusyYesterday(preferredShop,neighbourhood):
    if len(preferredShop.historicQueue)<24*6:
        return(randomSlotPref(preferredShop,neighbourhood))
    else:
        time = randint(OPENING_TIME,CLOSING_TIME) + (randint(0,5)/6.)
        shop = choice(neighbourhood.shops)
        if shop.smartSlots[int(time*6)]<=0:
            key = {"shop":preferredShop,"slot":time}
        else:
            shop.smartSlots[int(time*6)] -= 1
            key = {"shop":shop,"slot":time}
        return(key)