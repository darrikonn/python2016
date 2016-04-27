def hangman(path, state, guessed):
    myFile = open(path, 'r')
    stateLength = len(state)
    wordList = []
    for word in myFile.read().splitlines():
        if word != word.lower() or "'" in word or not word.encode("ascii", "ignore").decode("ascii") == word:
            continue
        isWord = False
        if len(word) == stateLength:
            isWord = True
            for i, n in enumerate(word):
                if not((state[i] == '-' and n not in guessed) or state[i] == n):
                    isWord = False
                    break
            if isWord:
                wordList.append(word)

    myFile.close()
    return wordList
