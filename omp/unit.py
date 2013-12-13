import multiprocessing

# private
# create new threading unit
def _newUnit(*args, **kwargs):
    return multiprocessing.Process(*args, **kwargs)

# private
# create new event object
def _newEvent(*args, **kwargs):
    return multiprocessing.Event(*args, **kwargs)

# private
# get a reference to the threading unit that is currently executing
def _currentUnit(*args, **kwargs):
    return multiprocessing.current_process()

# private
# get or set the name of the current threading unit
def _currentName(name=None):
    if name == None:
        return multiprocessing.current_process().name
    else:
        multiprocessing.current_process().name = name

# get the name of the current threading unit
def getUnitName():
    return multiprocessing.current_process().name
