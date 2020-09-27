import logging
import logging.handlers as handlers
import sys
import os
from functools import wraps
import traceback
import io


fmt = '''%(asctime)s -- %(levelname)s, 
    Message: %(message)s'''


class wwc_log:
    """
    maxsize: 单个文件的最大字节数\n
    loglevel: DEBUG, INFO...\n
    clean: 是否要清除之前的log文件\n
    """
    def __init__(self, maxsize=1024 * 1024, loglevel=logging.WARNING, clean=False):
        self.clean = clean
        self.maxsize = maxsize
        self.loglevel = loglevel

    def __call__(self, original):
        outer = self

        class inner:
            def __init__(self, original):
                self.format = logging.Formatter(
                    fmt, datefmt="%Y-%m-%d  %H:%M:%S")
                self.original = original
                self.__doc__ = original.__doc__
                self.logger: logging.Logger = logging.getLogger("wwc_log")
                self.logger.setLevel(outer.loglevel)
                self.rootDir = os.path.join(os.getcwd(),"tmp", "log")
                print('here', self.rootDir)
                self.logFileName = os.path.join(self.rootDir, "{}.txt".format(
                    self.original.__qualname__))

                try:
                    os.makedirs(self.rootDir)
                except:
                    pass

                try:
                    fileSize = os.path.getsize(self.logFileName)
                    if fileSize > outer.maxsize:
                        self._clean_log_flie()
                    if outer.clean:
                        self._clean_log_dir()
                except:
                    pass

                self.hander = logging.handlers.RotatingFileHandler(
                    self.logFileName, mode='a')
                self.hander.setFormatter(self.format)

                self.logger.addHandler(self.hander)

            def _clean_log_flie(self):
                with open(self.logFileName, 'w'):
                    pass

            def _clean_log_dir(self):
                allFiles = (os.path.join(self.rootDir, eachFile)
                            for eachFile in os.listdir(self.rootDir))
                for file in allFiles:
                    try:
                        os.remove(file)
                    except:
                        pass

            def __call__(self, *args, **kwargs):
                try:
                    self.logger.info("Begin: {}".format(
                        self.original.__qualname__))
                    res = self.original(*args, **kwargs)
                    self.logger.info("Exiting: {}".format(
                        self.original.__qualname__))
                    return res 
                except Exception:
                    msg = io.StringIO()
                    traceback.print_exc(file=msg)
                    msg.write("Function Name: {}".format(
                        self.original.__qualname__))
                    msg.write("\n\n\n\n")
                    self.logger.error(msg.getvalue())
        return inner(original)
