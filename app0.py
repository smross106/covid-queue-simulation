def blind(shop):
    queue = len(shop.queue)
    return(shop)

def block(shop):
    queue = len(shop.queue)
    if queue>shop.throughput:
        return(None)
    else:
        return(shop)