import atexit
from time import time


def secondsToStr(t):
    return str(round(t, 3))

line = "="*40


def log(s, elapsed=None):
    print()
    print(line)
    if elapsed:
        print("Time :", elapsed, "seconds")
    print(line)
    print()


def endlog():
    end = time()
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))

start = time()
atexit.register(endlog)