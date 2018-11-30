import re
def spell_check(path, s):
    exclude = '\"\',.;:!?%()'
    if s[0] in exclude:
        string = ''
    else:
        string = s[0]
    for i in range(1, len(s)):
        if s[i] in exclude:
            if i+1 < len(s):
                if s[i] == '.' and s[i-1].isdigit() and s[i+1].isdigit():
                    string += s[i]
        else:
            string += s[i]
    lis = []
    with open(path, 'r') as p:
        pr = set(p.read().lower().splitlines())
        for i, n in enumerate(string.split()):
            if not n.lower() in pr:
                lis.append(n)
    return lis
