from re import findall as F
from builtins import len as L
from builtins import int as I
def extract(s):
    N = None
    s = ' '.join(''.join(s.split()))
    l = F('[OsMSl]+|\\d+', s)
    if F('\w+|\\d+', s) != l:
        return N
    O = 'O0'
    f = []
    i = 0
    while i < L(l):
        e = l[i]
        if e in 'l1':
            if l[i+1] in O:
                f.append('10')
                i += 2
                continue
            else:
                return N
        if e.isdigit() < 4:
            if I(e) < 4:
                return N
        if e in O:
            return N
        f.append(e.upper())
        i += 1
    return f
