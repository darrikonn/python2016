from itertools import combinations
from itertools import product

def concatenate(s):
    n = len(s)
    comb = []
    for i in range(0, n):
        for j in combinations(range(1, n), i):
            comb.append(j)
    lis = []
    for i, e in enumerate(comb):
        e = (0,) + e
        lis.append([])
        for j in range(len(e)-1):
            lis[i].append(int(''.join(map(str, s[e[j]:e[j+1]]))))
        lis[i].append(int(''.join(map(str, s[e[len(e)-1]:]))))
    return lis

def operations(n):
    return list(product(['+', '-'], repeat=n))

def insert_operators(eqn, target):
    lis = concatenate(eqn)
    for i, e in enumerate(lis):
        oper = operations(len(e)-1)
        for j, o in enumerate(oper):
            summ = e[0]
            s = str(e[0])
            for k, p in enumerate(o):
                if p == '-':
                    summ -= e[k+1]
                    s = '{0}-{1}'.format(s, str(e[k+1]))
                else:
                    summ += e[k+1]
                    s = '{0}+{1}'.format(s, str(e[k+1]))
            if summ == target:
                return '{0}={1}'.format(s, str(target))
    return None
