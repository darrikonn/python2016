def birthdays(s):
    lis = s.split()
    length = len(lis)
    doneList = []
    birthdayList = []
    for i in range(length):
        tempList = []
        first4 = lis[i][:4]
        if doneList.count(first4) > 0:
            continue
        for j in range(i, length):
            if lis[j][:4] == first4:
                tempList.append(lis[j])
        if len(tempList) > 1:
            birthdayList.append(tempList)
        doneList.append(first4)
    return birthdayList
