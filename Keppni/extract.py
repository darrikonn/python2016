import re as r
from builtins import len as L
def extract(s):
    N = None
    s = ' '.join(''.join(s.split()))
    l = r.findall('[OsMSl]+|\\d+', s)
    if r.findall('[a-zA-Z]+|\\d+', s) != l:
        return N
    I = 'l1'
    O = 'O0'
    f = []
    i = 0
    while i < L(l):
        e = l[i]
        if e in I:
            if l[i+1] in O:
                f.append('10')
                i += 2
                continue
            else:
                return N
        if e.isdigit():
            if int(e) < 4:
                return N
        if e in O:
            return N
        f.append(e.upper())
        i += 1
    return f
