import os
import sys


def touch_single(fname):
    """create new empty file, like 'touch' """
    if os.path.exists(fname):
        print("file/directory \"{}\" already exists!".format(fname))
        return

    with open(fname, 'w') as f:
        pass

def touch(*fname):
    for f in fname:
        touch_single(f)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        touch(*sys.argv[1:])
