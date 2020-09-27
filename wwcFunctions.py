import random
import sys
from collections.abc import Iterable
import string
import warnings
from python_tools.dev_utils.count_empty_space import count_start_empty_space
from python_tools.dev_utils.functions import quote_in_quote


"""
some small general independent functions
"""


def __swim(arr, ix, key=lambda x: x):
    if ix <= 0:
        return
    p_ix = (ix - 1)//2
    if key(arr[p_ix]) > key(arr[ix]):
        arr[ix], arr[p_ix] = arr[p_ix], arr[ix]
        __swim(arr, p_ix, key)


def __sink(arr, ix, key=lambda x: x):
    if 2*ix + 1 >= len(arr):
        return
    l_ix = 2*ix + 1
    r_ix = l_ix + 1 if l_ix < len(arr)-1 else l_ix
    if key(arr[r_ix]) < key(arr[l_ix]):
        min_ix = r_ix
    else:
        min_ix = l_ix
    if key(arr[ix]) > key(arr[min_ix]):
        arr[ix], arr[min_ix] = arr[min_ix], arr[ix]
        __sink(arr, min_ix, key=key)


def __check_valid_codeblock(line: str, st: list, has_longmark=False):
    for mark in ('"""', "'''"):
        if mark not in line:
            continue
        has_longmark = True
        mark_ix = line.find(mark)
        if not quote_in_quote(line, mark, mark_ix):
            if (len(st) != 0 and mark != st[-1]) or (len(st) == 0):
                st.append(mark)
            else:
                st.pop()
            __check_valid_codeblock(line[mark_ix+1:], st, has_longmark=True)

    if has_longmark:
        return
    for mark in ('"', "'"):
        if mark not in line:
            continue
        mark_ix = line.find(mark)
        if not quote_in_quote(line, mark, mark_ix):
            if (len(st) != 0 and mark != st[-1]) or (len(st) == 0):
                st.append(mark)
            else:
                st.pop()
            __check_valid_codeblock(line[mark_ix+1:], st)


# public functions

def flatten(l, level=None):
    """ 
    Recursively flatten l, returns a 1-d list

    l: the input list (iterable) 
    level: how many layers to flatten, default is FLOAT_MAX
    """
    # if string, return directly
    if isinstance(l, str):
        return l
    level = int(sys.float_info.max) if level is None else level
    res = []
    for item in l:
        if isinstance(item, Iterable) and not isinstance(item, str) and level > 0:
            # string should not be flattened!!!
            res.extend(flatten(item, level - 1))
        else:
            res.append(item)

    return res


def equals(*args, key=None):
    if key is not None and not callable(key):
        raise AttributeError("key {} is not callable"
                             .format(key))
    if key is None:
        def key(x): return x

    if len(args) == 1:
        return True

    for i in range(1, len(args)):
        if key(args[i-1]) != key(args[i]):
            return False

    return True


def get_random_words(n):
    count = 0
    res = []
    chars = string.ascii_lowercase
    word = []
    random_interval = 10
    while count < n:
        for _ in range(random_interval):
            random.random()
        if random.random() < 0.8:
            for _ in range(random_interval):
                random.randrange(0, len(chars))
            this_char = chars[random.randrange(0, len(chars))]
            word.append(this_char)
            if len(word) > 10:
                count += 2
                res.append(''.join(word[:len(word)//2]))
                res.append(''.join(word[len(word)//2:]))
        else:
            if len(word) == 0:
                continue
            res.append(''.join(word))
            count += 1
            word.clear()
    return ' '.join(res)


def catch_warnings(callback=lambda: None, *args, **kwargs):
    def decorator(func):
        def wrapper(*args_, **kwargs_):
            with warnings.catch_warnings():
                warnings.filterwarnings('error')
                res = None
                try:
                    res = func(*args_, **kwargs_)
                except Warning as e:
                    print('caught: {}: {}'.format(type(e), e))
                    callback(*args, **kwargs)
                return res
        return wrapper
    return decorator


def read_class(clsname: str, lines, is_looking_for_override=False)->str:
    # raise DeprecationWarning('do not use it anymore')
    import re
    if not isinstance(lines, list):
        try:  # assume lines represent file
            with open(lines, 'r') as f:
                lines = f.readlines()
        except:
            raise
    found_class, found_override = False, False
    target = ('class', clsname)
    st = []
    source = []
    tab_size = -1  # 2 or 4
    class_tab = -1
    base_source = ''

    for line in lines:
        if line.strip() == '':
            continue
        if not found_class:
            __check_valid_codeblock(line, st)
            clsname_ix = line.find(clsname)
            if clsname_ix == -1 or len(st) != 0:  # not found
                continue
            comment_ix = line.find('#')
            if (comment_ix != -1) and (comment_ix < clsname_ix):
                continue
            if (not tuple(
                line.replace('(', ' ').split()[:2]) == target) \
                    and (not tuple(line.replace(':', ' ').split()[:2]) == target):
                continue
            if len(st) != 0:
                continue
            class_tab = count_start_empty_space(line)
            source.append(line)
            found_class = True
            # now parsing all base classes
            p = re.compile(r'\(+([\w,\.,\,,\s]+)\)+')
            match = p.search(line)
            bases = ['object']
            if match is not None:
                bases.append(*[cls.strip()
                               for cls in match.group(1).split(',')])
            for base in bases[1:]:  # apart from 'object'
                base_source += read_class(base, lines)

        else:
            line_tab = count_start_empty_space(line)
            if line_tab <= class_tab:
                break
            if is_looking_for_override:
                if not found_override:
                    if line.strip() == '@Override':
                        found_override = True
                        tab_size = line_tab - class_tab
                else:
                    if not line.strip().startswith('def'):
                        continue
                    source.append(line.strip('\n'))
                    source.append('{}pass'.format(
                        ' '*(tab_size+line_tab)))
                    found_override = False
            else:
                source.append(line.strip('\n'))
    return base_source + '\n'.join(source)


def minheapify(l, key=lambda x: x):
    size = len(l)
    i = 0
    while (2*i+1) < size:  # has children
        l_child_ix = 2*i + 1
        r_child_ix = l_child_ix + 1 if l_child_ix < size-1 else l_child_ix
        min_child_ix = -1

        if key(l[l_child_ix]) > key(l[r_child_ix]):
            min_child_ix = r_child_ix
        else:
            min_child_ix = l_child_ix

        if key(l[i]) > key(l[min_child_ix]):
            l[i], l[min_child_ix] = l[min_child_ix], l[i]  # switch
            __swim(l, i, key)
        i += 1


def copy_file(dst, src):
    _1G = 1 << 30
    with open(src, 'rb') as f1:
        with open(dst, 'wb') as f2:
            content = f1.read(_1G) 
            f2.write(content)

