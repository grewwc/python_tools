"""
when imported, register the 'root_dir' attribute in 'const'
"""
from python_tools import const


from . check_platform import (
    is_linux, is_mac, is_windows
)

__root_dir = None 


if is_linux() or is_mac():
    __root_dir = ('/')
else:
    __root_dir = tuple('C,D,E,F,G,H,c,d,e,f,g,h,/,\\'.split(','))

const.root_dir = __root_dir
