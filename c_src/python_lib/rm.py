import glob
import os
import shutil
import sys


def remove_single(file: str, recursive: bool, force: bool):
    """
    remove a single file
    no glob support in this funciton
    should not be used outside this file
    """

    if os.path.isfile(file):
        os.remove(file)
    elif os.path.isdir(file):
        if recursive:
            if force:
                shutil.rmtree(file)
            else:
                ans = None
                while True:
                    ans = input(
                        "do you want to delete '{}'? (y/n)".format(file)).lower()
                    if ans != 'y' and ans != 'n':
                        print("invalid choice")
                    else:
                        break
                if ans == 'y':
                    shutil.rmtree(file)


def remove_glob():
    """
    remove files from command line 
    can remove multiple files 
    only "-rf" is valid
    """

    if len(sys.argv) < 2:
        print("invalid argument")
        exit(1)
    files = sys.argv[1]
    positional_args = '-'
    if '-' in files:
        if len(sys.argv) <= 2:
            if files.strip() != "-h":
                print("invalid argument")
                exit(1)
            else:
                print(remove_glob.__doc__)
        files = sys.argv[2:]
        positional_args = sys.argv[1]
    else:
        files = [files]
    # only support "-rf"
    recurse, force = False, False
    if 'r' in positional_args:
        recurse = True
    if 'f' in positional_args:
        force = True
    for file in files:
        expand_files = glob.glob(file)
        if len(expand_files) == 0:
            print(f'cannot find file "{file}"')
        for f in expand_files:
            remove_single(f, recurse, force)


if __name__ == "__main__":
    remove_glob()
