import os
import argparse
from python_tools.dev_utils.touch import touch
from python_tools.dev_utils.count_empty_space import count_start_empty_space
from python_tools.small_components.terminal import cd
import shutil


class _File:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        if self.parent is not None:
            self.parent.children.append(self)
        self.children = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


def _build_dir_recurse(path: _File):
    if path.name.endswith('/'):  # path is directory
        path.name = path.name.strip('/') + '/'
        try:
            os.mkdir(path.name)
        except FileExistsError:
            if os.path.isfile(path.name):
                os.remove(path.name)
            elif os.path.isdir(path.name):
                shutil.rmtree(path.name)
            os.mkdir(path.name)
        if not path.children:
            return
        for sub_dir in path.children:
            with cd(path.name):
                _build_dir_recurse(sub_dir)
    else:  # path is normal file
        touch(path.name)


def build_dir():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', nargs=1, default=['build.txt'],
                        help='build directory according to a text file')
    parsed_args = parser.parse_args()
    cur_dir = os.getcwd()
    cur_empty_space = -1
    dummy = _File('dummy', None)
    cur_node = dummy
    with open(os.path.join(cur_dir, parsed_args.file[0])) as f:
        for line in f:
            if line.strip() == '':
                continue
            start_empty_space = count_start_empty_space(line)
            line = line.strip()
            if start_empty_space == cur_empty_space:
                cur_node = _File(line, cur_node.parent)
            elif start_empty_space > cur_empty_space:
                cur_node = _File(line, cur_node)
                if cur_node.parent and cur_node.parent.name.strip('/') != 'dummy':
                    cur_node.parent.name += '/'
            else:
                cur_parent = cur_node.parent.parent
                cur_node = _File(line, cur_parent)

            cur_empty_space = start_empty_space

    while cur_node and cur_node.name != 'dummy':
        cur_node = cur_node.parent

    for p in cur_node.children:
        _build_dir_recurse(p)


if __name__ == '__main__':
    build_dir()
