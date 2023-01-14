#!../venv/bin/python3
import sys
import os

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
    if data is None:
        with type_lock:
            if data is None:
                try:
                    data = board.get_contents(getattr(pasteboard, type_name))
                    if data is not None and len(data) > 0:
                        t = type_name
                except Exception as e:
                    print(e)
                    pass
                finally:
                    latch.count_down()


def write_to_file(data, filename):
    if not data:
        return
    mode = 'w' if t == 'String' else 'wb'
    if os.path.exists(filename):
        ans = input('filename: {} exists, overwrite? (y/n) ')
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
    latch = CountDownLatch(4)
    for type_name in supported_types:
        p.submit(_get_content_type, type_name, latch)
    latch.wait()
    if data is None:
        print("can't read from clipboard")
        return
    return data


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
        return


def check_input(args, positional):
    if not args.copy and args.binary:
        return False, 'paste from clipboard no argument'
    if len(positional) != 1:
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

    filename = positional[0]
    if copy:
        copy_from_file(filename, binary)
        print('<<< Done copying to clipboard')
    else:
        write_to_file(get_contents(), filename)
        print('>>> Done pasting from clipboard')


if __name__ == '__main__':
    main()
