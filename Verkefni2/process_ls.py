def process_ls(output):
    lis = output.split('\n')
    newList = []
    cp = lis.copy()
    for l in cp:
        if l[0] != 'd':
            newList.append(l.split()[4:])
    newList.sort(key=lambda x: x[4])
    newList.sort(key=lambda x: int(x[0]), reverse=True)

    return [' '.join(el[4:]) for el in newList]
