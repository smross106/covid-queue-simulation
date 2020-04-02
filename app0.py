def blind(shop):
    queue = len(shop.queue)
    return(True)

def block(shop):
    queue = len(shop.queue)
    if queue>shop.throughput:
        return(False)
    else:
        return(True)