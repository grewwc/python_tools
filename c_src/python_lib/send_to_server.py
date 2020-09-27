import subprocess
import sys
import os

ip = "147.8.146.85"
username = 'wwc129'


def send_single(filename, username, directory):
    print(f"sending:  {filename}")
    os.system(f'scp {filename} {username}@{ip}:{directory}')
   

def send(dirname, username,  directory):
    if os.path.isfile(dirname):
        send_single(dirname, username, directory)
        return

    files = [os.path.join(dirname, f) for f in os.listdir(dirname)]
    for f in files:
        send(f, username, directory)


if __name__ == '__main__':
    l = len(sys.argv)
    if l == 1 or l > 3:
        print("usage: ")
        print("\tsend sample.txt [~]")
        sys.exit(1)

    filename = sys.argv[1]
    directory = '~'
    if l == 3:
        directory = sys.argv[2]

    send(filename, username, directory)
