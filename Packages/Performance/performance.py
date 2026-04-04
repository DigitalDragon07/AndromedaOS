from time import clock, time 
import calendar


showLog = True
doLog = False

def timelog(func):
    def inner(*args, **kwargs):
        t1 = clock()
        result = func(*args, **kwargs)
        t2 = clock()
        print "[PERFORMANCE TEST] time for \"{}\" was {}".format(func.__name__, round(t2-t1, 5))
        return result
    return inner

def log():
    pass
print time()
print calendar.day_name