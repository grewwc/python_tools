import os
import sys
from .wwctime import timeit
import stat

counts = 0
extensions = ('.py', '.cpp', '.plist', '.js', '.txt', '.h', '.c', '.tex', '.html', '.css', '.java')
home = os.path.expanduser('~')


def match_sentence(filename: str, sentence: str):
    """sentence should be single line"""
    global counts
    try:
        with open(filename, 'r', encoding='utf8') as f:
            for lineno, line in enumerate(f, 1):
                if sentence in line:
                    counts += 1
                    print("{}:    {}\n".format(filename, lineno))
    except:
        pass


@timeit
def find(sentence, root_dir=home, limit=10):
    stack = []
    try:
        for f in os.listdir(root_dir):
            f = os.path.join(root_dir, f)
            finfo = os.lstat(f).st_mode
            if stat.S_ISLNK(finfo):
                continue
            if f.endswith(extensions) and stat.S_ISREG(finfo):
                if counts > limit:
                    return
                match_sentence(f, sentence)
            elif stat.S_ISDIR(finfo):
                stack.append(f)
                while stack:
                    if counts > limit:
                        return
                    cur_root_dir = stack.pop()
                    try:
                        for cur_f in os.listdir(cur_root_dir):
                            cur_f = os.path.join(cur_root_dir, cur_f)
                            cur_finfo = os.lstat(cur_f).st_mode
                            if stat.S_ISLNK(cur_finfo):
                                continue
                            if cur_f.endswith(extensions) and counts < limit and stat.S_ISREG(cur_finfo):
                                match_sentence(cur_f, sentence)
                            elif stat.S_ISDIR(cur_finfo):
                                stack.append(cur_f)
                    except:
                        pass
    except:
        pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("should have at least 1 parameters")
        print("1: sentence.  2: (optional, $HOME) root_dir.  3:(optional) limit")
        sys.exit(-1)

    else:
        find(*sys.argv[1:])
