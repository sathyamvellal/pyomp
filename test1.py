from omp import Omp
import time

@Omp.Parallel({"noThreads":3})
def foo():
    """@Omp.Single
    def foo1():
        print "Hello from single!"
        @Omp.Task
        def foo11():
            print "World from task!"
        print "Goodbye from single!"
    
    @Omp.For(range(13))
    def foo2(List):
        for item in List:
            print "item: %s" % item

    """
    @Omp.Sections
    def foo3():
        @Omp.Section
        def bar1():
            print "Section 1"
        @Omp.Section
        def bar2():
            print "Section 2"
        @Omp.Section
        def bar3():
            print "Section 3"
    
    print "Foo"
