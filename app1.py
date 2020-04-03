from random import randint,choice

#Standard advanced slot protocol:
#key = {
# "shop":shop,
# "slot":time code (hour)}

OPENING_TIME = 6
CLOSING_TIME = 22

#The following are for assigning slots to Actors
def randomSlotPref(preferredShop,neighbourhood):
    time = randint(OPENING_TIME,CLOSING_TIME) + (randint(0,5)/6.)
    key = {"shop":preferredShop,"slot":time}
    return(key)