import os
import sys
import time
import math
import numpy as np

os.system('clear')

# user input
path = str(sys.argv[1])
text = open(path).readlines()[0]
L = int(sys.argv[2])

# construct problem
words = [''] + text.split(' ')
c = [len(i) for i in words]
A = np.zeros((len(words),len(words)))
for i in range(len(A)):
    for j in range(len(A)):
        if i < j:
            l = sum(c[k] + 1 for k in range(i+1, j)) + c[j]
            A[i,j] = (L - l)**2


def dijkstras(A, s=0):
    d = [float('inf')] * len(A)
    p = [float('nan')] * len(A)
    S, F = [], []
    F.append(s)
    d[s] = 0
    while len(F) > 0:
        F.sort(reverse=True, key=lambda x: d[x])
        f = F.pop()
        S.append(f)
        for w in range(len(A)):
            if A[f][w] != 0:
                if w not in S and w not in F:
                    d[w] = d[f] + A[f][w]
                    p[w] = f
                    F.append(w)
                else:
                    if d[f] + A[f][w] < d[w]:
                        d[w] = d[f] + A[f][w]
                        p[w] = f

        # print to terminal
        os.system('clear')
        path = []
        j = len(p) - 1
        while not math.isnan(p[j]):
            path[0:0] = [p[j]]
            j = p[j]
        for i in range(len(path)-1):
            print(' '.join(words[path[i]+1:path[i+1]+1]))
        time.sleep(0.05)


while 1 > 0:
    dijkstras(A,0)
