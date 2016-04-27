from builtins import sorted as s
def flatten(l):
    return [s(l).index(x) for x in l]
