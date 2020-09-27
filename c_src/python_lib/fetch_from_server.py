import subprocess
import sys
import os

ip = "147.8.146.85"
username = 'wwc129'


def fetch_single(filename, username, directory):
    s = f'scp {username}@{ip}:{filename} {directory}'
    print(f"executing:  {s}")
    os.system(s)
   


if __name__ == '__main__':
    l = len(sys.argv)
    if l == 1 or l > 3:
        print("usage: ")
        print("\tsend sample.txt [~]")
        sys.exit(1)

    filename = sys.argv[1]
    directory = '.'
    if l == 3:
        directory = sys.argv[2]

    fetch_single(filename, username, directory)
