from functools import lru_cache
from python_tools.wwcFunctions import read_class
import sys
import os
import inspect
import re

@lru_cache()
def __read_file(name):
    with open(name) as f:
        return f.readlines()


def __get_import(lines: list)->str:
    source = []
    for line in lines:
        if line.strip().startswith('import') or \
            line.strip().startswith('from'):
            source.append(line.strip('\n'))
    return '\n'.join(source)


def Override(func):
    try:
        clsname, funcname = func.__qualname__.split('.')[-2:]
    except AttributeError:
        print("Ignore staticmethod AND classmethod!")
        return func

    modulename = inspect.getsourcefile(func)
    all_code = __read_file(modulename)
    import_source = __get_import(all_code)
    source = read_class(clsname, all_code, True)
    source = import_source + '\n' + source
    # print(source)
    exec(source)
    cls = locals()[clsname]
    bases = cls.__bases__
    for base in bases:
        if hasattr(base, funcname):
            return func
    bases = [base.__name__.split('.')[-1] for base in bases]
    raise AttributeError('No Method called "{}" in "{}"'
                         .format(funcname, bases))



def override(func):
    print(dir(func))
    print(func.__qualname__)
    print(func.__globals__.keys())
    return func