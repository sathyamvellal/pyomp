from omp import Omp
import omp.unit as unit
import time
import random
import sys

size = int(sys.argv[1])
A = [[random.random()*100 for i in range(size)] for j in range(size)]
B = [[random.random()*100 for i in range(size)] for j in range(size)]
C = [[0.0 for i in range(size)] for j in range(size)]

def multiply(A, B, C):
    for i in range(size):
        for j in range(size):
            for k in range(size):
                C[i][k] += A[i][k] * B[k][j]

t1 = time.time()
multiply(A, B, C)
t2 = time.time()
print (t2 - t1)

t3 = time.time()
@Omp.Parallel({"noThreads":4})
def foo():
    @Omp.For(range(size))
    def foo1(List):
        for i in List:
            for j in range(size):
                C[i][j] = 0
                for k in range(size):
                    C[i][j] += A[i][k] * B[k][j]
t4 = time.time()
print (t4 - t3)
