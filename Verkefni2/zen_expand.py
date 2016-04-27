import re
def zen_expand(html):
    myList = html.split('>')
    s = ''
    for i, n in enumerate(myList[::-1]):
        tempList = re.findall('[a-zA-Z]+|\\d+', n)[::-1]
        print(tempList)
        for j, el in enumerate(tempList):
            if j != 0 and tempList[j-1].isdigit():
                continue
            elif j == 0:
                if el.isdigit():
                    temp = '<' + tempList[j+1] + '>' + s + '</' + tempList[j+1] + '>'
                    tempString = ''
                    for k in range(int(el)):
                        tempString += temp
                    s = tempString
                else:
                    s = '<' + el + '>' + s + '</' + el + '>'
            else:
                if el.isdigit():
                    temp = '<' + tempList[j+1] + '></' + tempList[j+1] + '>'
                    tempString = ''
                    for k in range(int(el)):
                        tempString += temp
                    s = tempString + s
                else:
                    s = '<' + el + '></' + el + '>' + s
    return s
