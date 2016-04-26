def mod_sum(a):
    if a < 3:
        return 0
    summ = 0
    for i in range(1, a):
        if i % 5 == 0:
            summ += i
        elif i % 3 == 0:
            summ += i
    return summ
