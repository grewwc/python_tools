import os
import sys
import argparse
import colorama
from colorama import Fore
from fnmatch import fnmatch
from glob import glob

from contextlib import contextmanager


colorama.init()


@contextmanager
def color(colorname):
    try:
        colorObj = getattr(Fore, colorname.upper())
        print(colorObj, end='')
        yield
    finally:
        print(Fore.RESET, end='')


def print_file(filename, show_filename=False):
    try:
        if show_filename:
            with color('green'):
                print(f'\n\n=============>  {filename}\n')
        with open(filename, 'r', errors='ignore') as f:
            for line in f:
                print(line, end='')
    except Exception:
        with color('red'):
            print("cannot open file \"{}\"".format(filename))


def find_all_file(root, pattern):
    for root, dirs, files in os.walk(root):
        for f in files:
            if fnmatch(f, pattern):
                yield os.path.join(root, f).replace('\\', '/')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--recursive', '-r', action='store_true')
    parser.add_argument('--max', default=-1)
    all_args = parser.parse_known_args()
    args, filenames = all_args

    for filename in filenames:
        if args.recursive:
            for f in find_all_file('.', filename):
                print_file(f, True)

        else:
            print_file(filename, True)


if __name__ == '__main__':
    main()
