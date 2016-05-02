import shlex
def css_properties(css):
    myList = []
    lis = css.split(';')
    for i in range(len(lis)-1):
        el = lis[i].split(':')
        prev = ''.join(el[len(el)-2].strip().split()).split('{')
        print(prev)
        myList.append((prev[len(prev)-1], el[len(el)-1].strip()))
    return myList
