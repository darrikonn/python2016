import re
def jam(s):
    myMap = {}
    lis = s.splitlines()
    for i, n in enumerate(lis):
        my_string = ''.join(n[n.index(',')+1:n.rindex(',')].strip())
        allLower = [x for x in my_string.split() if x[0].islower()]
        for j, el in enumerate(allLower):
            my_string = my_string.replace(' ' + el, ',')
        l = [x.strip() for x in my_string.split(',')]
        for j, el in enumerate(l):
            if not el:
                continue
            if el in myMap:
                myMap[el] += 1
            else:
                myMap[el] = 1
    return myMap
