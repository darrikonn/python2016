import datetime
from datetime import datetime as D
from builtins import int as I
from builtins import str as S
from builtins import enumerate as E
def valid(n):
    F = False
    d = I(n[:2])
    m = I(n[2:4])
    y = n[4:6]
    r = I(n[6:8])
    c = I(n[9])
    if r < 20 or not (c == 0 or c == 9):
        return F
    try:
        if c == 0:
            y = I(S(20) + y)
        else:
            y = I(S(19) + y)
        D(y, m, d)
    except:
        return F
    s = 0
    x = [3, 2, 7, 6, 5, 4, 3, 2]
    for i,t in E(n[:8]):
        s += (x[i]*I(t))
    s = 11 - s % 11
    if s == 11:
        s = 0
    return s == I(n[8:9])
