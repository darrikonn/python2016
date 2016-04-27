from builtins import set as s
def duplicates(t):
    return [x for x in s(t) if x in t]
