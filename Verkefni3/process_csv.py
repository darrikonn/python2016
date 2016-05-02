from csv import reader
def process_csv(path):
    myFile = open(path, 'r')
    lis = myFile.read().splitlines()
    myMap = {}
    for n in reader(lis):
        val = int(n[2]) * int(n[3])
        if n[0] in myMap:
            myMap[n[0]] += val
        else:
            myMap[n[0]] = val
    return myMap
