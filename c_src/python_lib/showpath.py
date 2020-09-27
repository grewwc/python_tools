import os 
from typing import List
import sys 
import colorama
from colorama import Fore
from contextlib import contextmanager

@contextmanager
def color(color: str):
    try:
        colorObj = getattr(Fore, color.upper())
        print(colorObj, end='')
        yield 
    finally:
        print(Fore.RESET, end='')


colorama.init(convert=True)

def getPaths() -> list:
    res = os.getenv("path")
    res = res.split(";")
    return res



def match(line: str, pattern: str) -> bool:
    if pattern == '':
        return True

    return pattern in line


def printWordWithColor(line: str, word: str) -> None:
    if word == '':
        print(line)
        return 

    idx = line.index(word)

    print(line[:idx], end='')
    with color('red'):
        print(line[idx:idx+len(word)], end='')
    print(line[idx+len(word):])


def main():
    if len(sys.argv) == 1:
        pattern = ""
    else:
        pattern = sys.argv[1]

    paths = getPaths()
    for line in paths:
        if match(line, pattern):
            printWordWithColor(line, pattern)
            

if __name__ == '__main__':
    main()