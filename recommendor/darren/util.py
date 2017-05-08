
# Utility file
# For common methods
import datetime

# start timing
def start_time(name):
    t = datetime.datetime.now().time()
    if name is None:
        print("start: " t.isoformat()))
    else:
        print(name + " start: " t.isoformat())

# end timing
def end_time(name):
    t = datetime.datetime.now().time()
    if name is None:
        print("end: " t.isoformat()))
    else:
        print(name + " end: " t.isoformat())
