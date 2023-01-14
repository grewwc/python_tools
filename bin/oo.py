#!../venv/bin/python3
import sys
import os
import time 

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from argparse import ArgumentParser
from threading_utils import CountDownLatch
import pasteboard
from threading import RLock, Barrier
from concurrent.futures import ThreadPoolExecutor

board = pasteboard.Pasteboard()
supported_types = ['PDF', 'PNG', 'RTF', 'String', 'TIFF']
type_lock = RLock()
data = None
t = None


def _get_content_type(type_name, latch):
    if type_name not in supported_types:
        return None
    global data, t
    contents = board.get_contents(getattr(pasteboard, type_name))
    if data is None:
        with type_lock:
            if data is None and contents is not None:
                try:
                    data = contents
                    t = type_name
                except Exception as e:
                    print(e)
    latch.count_down()


def write_to_file(data, filename):
    if not data:
        return
    mode = 'w' if t == 'String' else 'wb'
    if os.path.exists(filename):
        ans = input('filename: {} exists, overwrite? (y/n) '.format(filename))
        if ans.lower() != 'y':
            print('skipping ...')
            return
    dirname = os.path.dirname(filename)

    if dirname and not os.path.exists(dirname):
        print('making dir: {}'.format(dirname))
        os.makedirs(dirname)
    with open(filename, mode) as f:
        f.write(data)


def get_contents():
    p = ThreadPoolExecutor(max_workers=4)
    latch = CountDownLatch(len(supported_types))
    for type_name in supported_types:
        p.submit(_get_content_type, type_name, latch)
    latch.wait()


def copy_from_file(filename, binary):
    mode = 'rb' if binary else 'r'
    try:
        with open(filename, mode) as f:
            data = f.read()
    except FileNotFoundError:
        print('file: {} not found'.format(filename))
        return 
    type_ = pasteboard.String if not binary else pasteboard.PNG
    success = board.set_contents(data, type_)
    if not success:
        print('error copy to clipboard')
        return False


def check_input(args, positional):
    if not args.copy and args.binary:
        return False, 'paste from clipboard no argument'
    if len(positional) != 1 and args.copy:
        return False, 'set the filename'
    return True, ''


def main():
    parser = ArgumentParser()
    parser.add_argument("--copy", "-c", action="store_true", help="copy to clipboard")
    parser.add_argument("--binary", '-b', action="store_true", help="binary file")
    args, positional = parser.parse_known_args()

    valid_input, msg = check_input(args, positional)
    if not valid_input:
        print(msg)
        return

    copy = True if args.copy else False
    binary = True if args.binary else False

    filename = 'temp.png' if len(positional) < 1 else positional[0]
    if copy:
        if not copy_from_file(filename, binary):
            return 
        print('<<< Done copying to clipboard')
    else:
        get_contents()
        if data is None:
            print("can't read from clipboard")
            return 
        write_to_file(data, filename)
        print('>>> Done pasting from clipboard')


if __name__ == '__main__':
    main()
