from pyjpgclipboard import clipboard_dump_jpg, clipboard_load_jpg
import pyperclip
from argparse import ArgumentParser
import sys
import os
from PIL import ImageGrab


data = None
t = None
force = False


def write_to_file(data, filename, is_binary: bool = False):
    if not data:
        return
    mode = 'w' if not is_binary else 'wb'
    if os.path.exists(filename):
        if not force:
            ans = input('filename: {} exists, overwrite? (y/n) '.format(filename))
            if ans.lower() != 'y':
                print('skipping ...')
                return
        else:
            print('overwrite {}'.format(filename))

    dirname = os.path.dirname(filename)

    if dirname and not os.path.exists(dirname):
        print('making dir: {}'.format(dirname))
        os.makedirs(dirname)
    with open(filename, mode) as f:
        f.write(data)


def clipboard_to_file(filename, binary: bool):
    global data
    if binary:
        try:
            im = ImageGrab.grabclipboard()
            im.save(filename)
            return True
        except:
            print('No image in clipboard.')
            return False
    else:
        try:
            data = pyperclip.paste()
            write_to_file(data, filename, binary)
            return True
        except Exception as e:
            print(e)
            return False


def copy_from_file(filename, binary):
    if not os.path.exists(filename):
        print('{} not exist'.format(filename))
        return
    if binary:
        try:
            clipboard_load_jpg(filename)
        except Exception as e:
            print(e)
            return False
    else:
        try:
            with open(filename, 'r') as f:
                data = f.read()
                pyperclip.copy(data)
        except Exception as e:
            print(e)
            return False
    return True


def main():
    global force
    parser = ArgumentParser()
    parser.add_argument("--copy", "-c", action="store_true", help="copy to clipboard")
    parser.add_argument("--paste", "-p", action="store_true", help="paste from clipboard")
    parser.add_argument("--binary", '-b', action="store_true", help="binary file")
    parser.add_argument("--force", "-f", action="store_true", help="force override")
    args, positional = parser.parse_known_args()
    copy = True if args.copy else False
    binary = True if args.binary else False
    force = True if args.force else False
    paste = True if args.paste else False
    if len(sys.argv) == 1:
        parser.print_help()
        return

    if len(positional) == 1:
        filename = positional[0]
    elif len(positional) == 0:
        filename = input('filename: ')
    else:
        raise Exception("too many positional args: {}".format(positional))

    filename = os.path.expanduser(filename)
    if copy:
        if not copy_from_file(filename, binary):
            return
        print('<<< Done copying to clipboard')
    else:
        res = clipboard_to_file(filename=filename, binary=binary)
        if res:
            print('>>> Done pasting from clipboard')
        else:
            print(">>> can't paste from clipboard")


if __name__ == '__main__':
    main()
