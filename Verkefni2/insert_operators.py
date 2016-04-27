def insert_operators(eqn, target):
    # +-concatenate
    combinations = []
    myList = []
    cnt = 1
    while 1:
        per = concatenate(eqn, cnt)
        cnt += 1
        combinations.append(per)
        if len(per) == 1:
            break
    #for i, n in enumerate(combinations):


    return combinations

def concatenate(lis, n):
    res = []
    isFull = False
    for i in range(0, len(lis)):
        s = ''
        for j in range(n):
            if j + i == len(lis):
                isFull = True
                break
            s += str(lis[i+j])
        if isFull:
            break
        res.append(s)
    return res
