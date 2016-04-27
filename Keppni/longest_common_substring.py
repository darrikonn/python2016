from builtins import range as R
from builtins import len as L
from builtins import all as A
def longest_common_substring(l):
    c = 0
    for i in R(L(l[0])):
        for j in R(1, L(l[0])+1):
            w = l[0][i:i+j]
            if L(w) > c and A(w in x for x in l):
                c = L(w)
    return c
