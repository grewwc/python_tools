import os
import re
import argparse


def _show_path(path, name_pattern, is_reg=True, ignore_case=False):
    try:
        if os.path.isfile(path):
            base_name = os.path.basename(path)
            if not is_reg:
                if ignore_case:
                    base_name, name_pattern = base_name.upper(), name_pattern.upper()
                if base_name == name_pattern:
                    print(path)
            elif is_reg and name_pattern.match(base_name) is not None:
                print(path)
        elif os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                _show_path(os.path.join(path, file), name_pattern, is_reg)
    except:
        pass 

def find(from_dir, name: str, ignore_case):
    regex = True
    if '*' not in name and '?' not in name:
        regex = False
    name = name.replace('*', '.*').replace('?', '.')
    from_dir = os.path.expanduser(from_dir)
    if not ignore_case:
        p = re.compile(name) if regex else name
    else:
        p = re.compile(name, re.I) if regex else name
    _show_path(from_dir, p, regex)


def _parse_cmd_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('from_dir', action='store', type=str)
    parser.add_argument('filename', action='store', type=str)
    parser.add_argument('--ignore_case', '-i', action='store_true', 
        help='default is false')
    args = parser.parse_args()
    return args.from_dir, args.filename, args.ignore_case


if __name__ == '__main__':
    from_dir, name, ignore_case = _parse_cmd_args()
    find(from_dir, name, ignore_case)
