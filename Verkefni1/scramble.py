def scramble(a, b):
    myList = []
    for i in range(len(b)):
        myList.append(a[b[i]])

    return myList
