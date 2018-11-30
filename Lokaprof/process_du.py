import os
def process_du(s):
    lis = []
    for i, n in enumerate(s.splitlines()):
        lis.append(n.split(maxsplit=1))
    return [os.path.basename(x[1]) for x in sorted(lis, key=lambda x: int(x[0]), reverse=True)]
