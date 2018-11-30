from csv import reader
def acc_ascension(path):
    dic = {}
    with open(path, 'r') as p:
        for n in reader(p.read().splitlines()[4:]):
            key = n[2]
            value = int(n[4])
            if key in dic:
                dic[key] += value
            else:
                dic[key] = value
    return dic
