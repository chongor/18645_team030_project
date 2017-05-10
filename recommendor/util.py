
# Utility file
# For common methods
import datetime

# start timing
def start_time(name=None):
    t = datetime.datetime.now().time()
    if name is None:
        print("start: " + t.isoformat())
    else:
        print(name + " start: " + t.isoformat())

# end timing
def end_time(name=None):
    t = datetime.datetime.now().time()
    if name is None:
        print("done: " + t.isoformat())
    else:
        print(name + " done: " + t.isoformat())
