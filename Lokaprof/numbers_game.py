from itertools import permutations
def numbers_game(lis):
    possibilites = permutations(lis, 8)
    for i, n in enumerate(possibilites):
        if check_restrictions(n):
            return True
    return False

def check_restrictions(lis):
    for i in range(1, len(lis)):
        n = lis[i]
        prev = lis[i-1]
        # even
        if prev % 2 == 0:
            if not (prev == n or not n % 2 == 0):
                return False
        # odd
        else:
            if n > prev:
                if not n % 2 == 0:
                    return False
            elif n < prev:
                if n % 2 == 0:
                    return False
            else:
                return False
    return True
