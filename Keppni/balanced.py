def balanced(p):
    l = 0
    for i in p:
        if i == '(':
            l += 1
        elif l:
            l -= 1
        else:
            return False
    return not l
