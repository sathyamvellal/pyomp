import multiprocessing

def newUnit(*args, **kwargs):
    return multiprocessing.Process(*args, **kwargs)

def newEvent(*args, **kwargs):
    return multiprocessing.Event(*args, **kwargs)

def currentUnit(*args, **kwargs):
    return multiprocessing.current_process()

def currentName(name=None):
    if name == None:
        return multiprocessing.current_process().name
    else:
        multiprocessing.current_process().name = name
