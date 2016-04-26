import collections
def countdown(path, letters):
    letters = collections.Counter(letters)
    myFile = open(path, 'r')
    wordList = []
    for word in myFile.read().splitlines():
        if len(word) > 3:
            isWord = True
            for x in word:
                if not (letters.get(x) is not None and word.count(x) <= letters.get(x)):
                    isWord = False
                    break
            if isWord:
                wordList.append(word)
        #if len(word) > 3 and [word.count(x) <=  for x in word]:
         #   wordList.append(word)
    myFile.close()
    return sorted(wordList)
