from omp.unit import _newUnit, _newEvent, _currentUnit, _currentName
import types
import math
import time

# class that gives provides decorators for OpenMP-like constructs
#   hidden from import
#   contains states 
#       thread and an event object tied to the thread; used for creating barriers
# Instantiated at the end of the file
class _OmpFactory:

    # constructor
    def __init__(self):
        self._stateStack = [] # a stack to store current state to support nesting
        self._currentState = [] # current state
        pass

    # internal barrier function
    #   requires the previous state to be saved in the _stateStack and _currentState populated
    def _barrier(self):
        for i in range(len(self._currentState)):
            self._currentState[i][1].wait()
        self._currentState = self._stateStack.pop()
        for i in range(len(self._currentState)):
            self._currentState[i][1].set()

    # function to execute a func and fire events to waiting threads in the _currentState
    def _execFunc(self, func, *args, **kwargs):
        func(*args)
        self._currentState[int(unit._currentName()[1:])][1].set()
    
    # primary decorator
    # requires :
    #   noThreads - the number of threads to execute
    def Parallel(self, data):
        # if data is a function, then no data was passed to @Parallel. Don't apply the decorator
        #   don't return function as this is not supposed to be called in this way
        if type(data) == types.FunctionType:
            pass
        else: # data was passed, return another decorator to capture the function
            self._noThreads = data["noThreads"]
            unit._currentName("Main")
            def _Parallel(func):
                self._currentState.append((unit._currentUnit(), unit._newEvent()))
                for i in range(1, self._noThreads):
                    t, e = unit._newUnit(target=func, name=("P%d" % i)), unit._newEvent()
                    self._currentState.append((t,e))
                    t.start()
                func()
            return _Parallel

    # the for decorator
    # needs a list to be passed as a parameter
    #   this list is divided into chunks and the function is called passing the borken list in different threads
    # also requires the decorated function to accept only one argument which is the List
    #   this function "must" contain only one for loop, iterating over the list
    def For(self, List):
        self._stateStack.append(self._currentState)
        self._currentState = []
        if unit._currentName() == "Main":
            def _For(func):
                cs = int(math.ceil(float(len(List)) / self._noThreads))
                for i in range(self._noThreads):
                    t, e = unit._newUnit(target=self._execFunc, args=(func,List[cs*i:cs*i+cs],), name=("P%d" % i)), unit._newEvent()
                    self._currentState.append((t,e))
                    t.start()
                self._barrier()
        else:
            def _For(func):
                e = self._stateStack[0][int(unit._currentName()[1:])][1]
                e.wait()
        return _For
    
    # the single decorator
    #   guaranteed execution in one thread
    # can contain tasks inside
    def Single(self, func):
        self._stateStack.append(self._currentState)
        self._currentState = []
        if unit._currentName() == "Main":
            self._taskQueue = []
            self._sectionNext = 0
            func()
            for task in self._taskQueue:
                task.start()
            self._barrier()
        else:
            e = self._stateStack[0][int(unit._currentName()[1:])][1]
            e.wait()

    # Task decorator
    # must be applied insude a single construct
    def Task(self, func):
        t, e = unit._newUnit(target=self._execFunc, args=(func,), name=("P%d" % self._sectionNext)), unit._newEvent()
        self._sectionNext += 1
        self._currentState.append((t,e))
        self._taskQueue.append(t)

    # sections decorator 
    # also executes the given function 
    def Sections(self, func):
        self._stateStack.append(self._currentState)
        self._currentState = []
        if unit._currentName() == "Main":
            self._sectionNext = 0
            func()
            self._barrier()
        else:
            e = self._stateStack[0][int(unit._currentName()[1:])][1]
            e.wait()

    # section decorator
    # to be used inside a sections decorator
    # the decorated 
    def Section(self, func):
        t, e = unit._newUnit(target=self._execFunc, args=(func,), name=("P%d" % self._sectionNext)), unit._newEvent()
        self._sectionNext += 1
        self._currentState.append((t,e))
        t.start()

Omp = _OmpFactory() # Omp object constructed 
