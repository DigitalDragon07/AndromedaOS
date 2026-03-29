from time import*


def log(func):
    def inner(*args, **kwargs):
        c1 = clock()
        func(*args, **kwargs)
        c2 = clock()
        print "DEBUG: time for {0} was {1}".format(func.__name__, c2-c1)
    return inner

timer = [0, 0]
def startTimer():
    global timer
    timer[0] = clock()
def endTimer():
    global timer
    timer[1] = clock()
    print "DEBUG: timer is {}".format(timer[1] - timer[0])
    timer = [0, 0]
def viewTimer():
    global timer
    now = clock()
    print "DEBUG: Timer is currently at {}".format(round(now - timer[0], 5))
    
startTimer()
viewTimer()