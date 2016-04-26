def rank_hand(lis):
    pairDict = list(map(list, zip(*lis)))
    keyList = pairDict[0]
    valueList = list([keyList.count(el) for el in set(keyList)])
    keyList = list(set(keyList))
    flushList = pairDict[1]
    isFlush = all(x == flushList[0] for x in flushList)
    isTwoPairs = valueList.count(2) > 1
    isOnePair = valueList.count(2) == 1
    isThreePair = valueList.count(3) == 1
    isFullHouse = isOnePair and isThreePair
    isFourPair = valueList.count(4) == 1
    hasAce = False
    isStraight = True
    if len(keyList) > 4:
        hasTwo = keyList.count('2') > 0
        for i, n in enumerate(keyList):
            if n == 'T':
                keyList[i] = '10'
            elif n == 'J':
                keyList[i] = '11'
            elif n == 'Q':
                keyList[i] = '12'
            elif n == 'K':
                keyList[i] = '13'
            elif n == 'A':
                if hasTwo:
                    keyList[i] = '1'
                else:
                    hasAce = True
                    keyList[i] = '14'
        keyList = list(map(int, keyList))
        keyList.sort()
        for c in range(1, len(keyList)):
            if keyList[c-1] + 1 != keyList[c]:
                isStraight = False
                break
    else:
        isStraight = False
    if hasAce and isFlush and isStraight:
        return 9
    elif isFlush and isStraight:
        return 8
    elif isFourPair:
        return 7
    elif isFullHouse:
        return 6
    elif isFlush:
        return 5
    elif isStraight:
        return 4
    elif isThreePair:
        return 3
    elif isTwoPairs:
        return 2
    elif isOnePair:
        return 1
    return 0
