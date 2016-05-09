from string import printable
from random import choice
import sys

sys.path.insert(0, '..')

_curr_dir = os.path.dirname(__file__)
_alnum_index = 62
_symbol_index = 94

def _words():
    word_file = os.path.join(_curr_dir, 'words.txt')
    with open(word_file) as f:
        return list(filter(str.isalpha(), f.read().splitlines()))

def pword(words=4, sep=' '):
    w = _words()
    return sep.join(choice(w) for _ in range(words))

def rand_pass(length=8, use_symbols=True):
    index = [_alnum_index, _symbol_index][use_symbols]
    return ''.join(choice(printable[:index]) for _ in range(length))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pass some words!')
    parser.add_argument('--count', '-c', default=5, type=int, help='How many passwords')
    parser.add_argument('--words', '-w', default=pword.__defaults__[0], type=int, help='Number of words in each password')
    parser.add_argument('--seperator', '-s', default=pword.__defaults__[1], help='Seperator')
    args = parser.parse_args()
    for _ in range(args.count):
        print(pword(args.words, args.seperator))
