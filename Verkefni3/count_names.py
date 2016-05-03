import urllib.request
import json
def count_names(s):
    names = json.loads(urllib.request.urlopen('https://mooshak.ru.is/~python/names.json').read().decode('utf-8'))
    f1 = 0
    f2 = 0
    for name in names:
        if name['Nafn'] == 0:
            name['Nafn'] = ''
        if name['Nafn'].startswith(s):
            f1 += name['Fjoldi1']
            f2 += name['Fjoldi2']
    return (f1, f2)
