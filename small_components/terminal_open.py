import platform
import sys

from python_tools.constants.platform_name import PlatformName
from python_tools.wwcFunctions import equals
import os


def _get_platform_name(name):
    if name == PlatformName.windows:
        return 'windows'
    if name == PlatformName.mac:
        return 'mac'
    if name == PlatformName.linux:
        return 'linux'
    return None


def open():
    """
    :return: None

    this file will be called by c++ code
    """
    platform_name = _get_platform_name(platform.system())
    if platform_name is None:
        raise NameError("platform name '{}' not supported"
                        .format(platform.system()))
    arg = sys.argv[-1]
    if equals(arg, __file__, key=os.path.basename):
        arg = '.'

    if platform_name == 'windows':
        os.system('start "" {}'.format(arg))
        return
    if platform_name == 'mac':
        os.system('open {}'.format(arg))
        return
    if platform_name == 'linux':
        os.system('xdg-open {}'.format(arg))
        return



if __name__ == '__main__':
    open()
