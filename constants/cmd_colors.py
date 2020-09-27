from .platform_name import PlatformName
import platform 
from python_tools.dev_utils.get_public_attrs import get_public_attrs

class ColorsMeta(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        sys_name = platform.system()
        if sys_name == PlatformName.windows:
            # don't show color in cmd 
            for color in get_public_attrs(cls):
                setattr(cls, color, '')


class colors(metaclass=ColorsMeta):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = "\033[0;0m"

    

