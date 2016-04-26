def palindrome(n, b):
    myList = []
    while n != 0:
        myList.append(int(n % b))
        n //= b
    return myList == myList[::-1]
