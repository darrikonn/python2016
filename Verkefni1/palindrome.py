def palindrome(n, b):
    if b == 2:
        n = bin(n)
        s = str(n)[2:]
        return s == s[::-1]
    if b == 16:
        n = hex(n)
        s = str(n)[2:]
        return s == s[::-1]
    if b == 8:
        n = oct(n)
        s = str(n)[2:]
        return s == s[::-1]
    return str(n) == str(n)[::-1]
