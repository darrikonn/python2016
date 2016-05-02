import os, sys
def parse_submissions(PATH):
    lis = []
    for root, dirs, files in os.walk(PATH):
        for f in files:
            path = os.path.join(root, f)
            try:
                with open(path) as cf:
                    lines = cf.read().splitlines()
                    date = lines[0].split()
                    problem = lines[1].split()
                    team = lines[2].split()
                    classify = lines[3].split()
                    if classify[2] == 'Accepted':
                        lis.append([date[2], team[2], problem[2]])
            except:
                sys.stderr.write('could not open\n' % path)
    return [(l[1], l[2]) for l in sorted(lis)]
