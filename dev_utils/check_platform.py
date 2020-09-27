import platform 
from python_tools.constants import platform_name
from python_tools import const

def is_windows():
    return platform.system() == const.windows 

def is_mac():
    return platform.system() == const.mac 

def is_linux():
    return platform.system() == const.linux
