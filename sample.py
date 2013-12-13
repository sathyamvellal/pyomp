from omp import Omp
import omp.unit as unit
import time
import random

@Omp.Parallel({"noThreads":4})
def foo():
    @Omp.Single
    def foo1():
        print ("Hello from single!")
        @Omp.Task
        def foo11():
            print ("World from task 1!")
        @Omp.Task
        def foo12():
            print ("World from task 2!")
        print ("Goodbye from single!")
    
    @Omp.For(range(8))
    def foo2(List):
        for item in List:
            print "Process: %s, item: %s" % (unit.getUnitName(), item)

    @Omp.Sections
    def foo3():
        @Omp.Section
        def bar1():
            print ("Section 1")
        @Omp.Section
        def bar2():
            print ("Section 2")
        @Omp.Section
        def bar3():
            print ("Section 3")
    
    print ("Foo")
