import unit
import types
import math

class State:
    def __init__(self, unit, event):
        self.unit = unit
        self.event = event

class _OmpFactory:
    def __init__(self):
        self._stateStack = []
        self._currentState = []
        pass

    def _barrier(self):
        for i in xrange(len(self._currentState)):
            self._currentState[i][1].wait()
        self._currentState = self._stateStack.pop()
        for i in xrange(len(self._currentState)):
            self._currentState[i][1].set()

    def _execFunc(self, func, *args, **kwargs):
        func(*args)
        self._currentState[int(unit.currentName()[1:])][1].set()
        
    def Parallel(self, data):
        # if data is a function, then no data was passed to @Parallel. Consider default settings
        if type(data) == types.FunctionType:
            self._noThreads = 4
            data()
        else: # data was passed, return another decorator to capture the function
            self._noThreads = data["noThreads"]
            unit.currentName("Main")
            def _Parallel(func):
                for i in xrange(self._noThreads):
                    t, e = unit.newUnit(target=func, name=("P%d" % i)), unit.newEvent()
                    self._currentState.append((t,e))
                    t.start()
                func()
            return _Parallel

    def For(self, List):
        self._stateStack.append(self._currentState)
        self._currentState = []
        if unit.currentName() == "Main":
            def _For(func):
                cs = int(math.ceil(float(len(List)) / self._noThreads))
                for i in xrange(self._noThreads):
                    t, e = unit.newUnit(target=self._execFunc, args=(func,List[cs*i:cs*i+cs],), name=("P%d" % i)), unit.newEvent()
                    self._currentState.append((t,e))
                    t.start()
                self._barrier()
        else:
            def _For(func):
                e = self._stateStack[0][int(unit.currentName()[1:])][1]
                e.wait()
        return _For

    def Single(self, func):
        self._stateStack.append(self._currentState)
        self._currentState = []
        if unit.currentName() == "Main":
            t, e = unit.newUnit(target=self._execFunc, args=(func,), name=("Main")), unit.newEvent()
            self._currentState.append((t,e))
            t.start()
            self._barrier()
        else:
            e = self._stateStack[0][int(unit.currentName()[1:])][1]
            e.wait()

    def Task(self, func):
        self._stateStack.append(self._currentState)
        self._currentState = []
        if unit.currentName() == "Main":
            for i in xrange(self._noThreads):
                t, e = unit.newUnit(target=self._execFunc, args=(func,), name=("P%d" % i)), unit.newEvent()
                self._currentState.append((t,e))
                t.start()
            self._barrier()
            unit.currentName("P0")
        else:
            e = self._stateStack[0][int(unit.currentName()[1:])][1]
            e.wait()

    def Sections(self, func):
        self._stateStack.append(self._currentState)
        self._currentState = []
        if unit.currentName() == "Main":
            self._sectionNext = 0
            func()
            self._barrier()
        else:
            e = self._stateStack[0][int(unit.currentName()[1:])][1]
            e.wait()

    def Section(self, func):
        t, e = unit.newUnit(target=self._execFunc, args=(func,), name=("P%d" % self._sectionNext)), unit.newEvent()
        self._sectionNext += 1
        self._currentState.append((t,e))
        t.start()

Omp = _OmpFactory()
