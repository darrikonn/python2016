def excel_index(s):
    indices = 0
    for i in range(len(s) - 1):
        indices += pow(26, len(s) - (i+1)) * (ord(s[i]) - 64)
    indices += (ord(s[-1]) - 64)
    return indices
