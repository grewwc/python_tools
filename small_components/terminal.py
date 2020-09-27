from contextlib import contextmanager
import os
import argparse
from python_tools.constants.cmd_colors import colors
import sys
import python_tools.dev_utils.root_dir
from python_tools import const


def __to_abs_path(original):
    if original in const.root_dir:
        return original
    return os.path.join(os.getcwd(), original)


@contextmanager
def cd(to: str):
    if not isinstance(to, str):
        raise TypeError("path {} is not a string".format(to))
    original_path = os.getcwd()
    to_abs_path = __to_abs_path(to)
    try:
        os.chdir(to_abs_path)
    except (FileNotFoundError, OSError, PermissionError) as e:
        print("Error here: ", e)
        raise
    try:
        yield
    except Exception as e:
        print(e)
        raise
    finally:
        os.chdir(original_path)


def _files_have_permission(files):
    """
    :param files: 要筛选的files
    :return: 有权限的文件
    """
    res = []
    import inspect
    frame = inspect.currentframe()
    this_func_name = inspect.getframeinfo(frame).function
    for file in files:
        try:
            os.path.getmtime(file)
        except OSError:
            pass
        except:
            print("unknown error in {}".format(this_func_name))
        else:
            res.append(file)
    return res


def _ls():
    all_files = os.listdir(os.getcwd())
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', '-n', type=int, default=20,
                        help='number of files to be printed')
    parser.add_argument('--all', '-a', action='store_true',
                        help='if show hidden files')
    # "parse_known_args" return a tuple
    parsed_args = parser.parse_known_args()[0]
    yield parser.parse_known_args()[1]  # in order to get the directory name

    # permission problem for "os.path.getmtime"
    all_files = _files_have_permission(all_files)
    all_files = sorted(all_files, reverse=True,
                       key=os.path.getmtime)
    num_of_file = 0
    selected_files = []

    parsed_args_num = parsed_args.num if parsed_args.num >= 0 else len(
        all_files)

    for i, f in enumerate(all_files):
        if parsed_args.all is False:
            if f.startswith('.'):
                continue
            num_of_file += 1
            selected_files.append(f)
            if num_of_file >= parsed_args_num:
                break
        else:
            selected_files = all_files[:parsed_args_num]

    for i, f in enumerate(selected_files):
        if os.path.isdir(f):
            print(colors.OKBLUE, end='')
            print('{:5d}: {} {}'.format(i + 1, f, colors.RESET))
        else:
            print('{:5d}: {}'.format(i + 1, f))


def ls():
    """terminal usage"""
    dir_name = next(_ls())
    assert len(dir_name) == 0 or len(dir_name) == 1, "parsing error!"
    dir_name = '.' if len(dir_name) == 0 else dir_name[0]
    with cd(dir_name):
        _ls_gen = _ls()
        next(_ls_gen)  # get the directory name, ignore the result
        try:
            next(_ls_gen)  # list all the files
        except StopIteration:
            pass


if __name__ == '__main__':
    ls()
