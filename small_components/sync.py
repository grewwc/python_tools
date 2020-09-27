import os
import datetime
import sys
import shutil
import time


class StopOperationException(Exception):
    pass


class Sync_To_Dropbox:
    '''
        1. If file in 'src' & not in 'dest', copy the file to 'dest'
        2. If the file is in both 'src' and 'dest', check the datetime. If the file is 
            changed within the last 'N' days. (N defaults to 1)
    '''
    num_of_sync_files = 0
    run_interval = 600
    stop = False

    def __init__(self,
                 src,
                 dest=None,
                 timedelta=datetime.timedelta(days=1),
                 backend_mode=False):
        '''
            src & dest should be Folder path
        '''
        self.backend_mode = backend_mode

        if dest == None:
            home: str = os.environ.get('HOME')
            if home == None and not self.backend_mode:
                print("'HOME' value is None")
            dest = os.path.join(home, 'Dropbox', 'Thesis')

        if src == None:
            src = dest

        self.errorProcess(src, dest)

        self.ignore_files = ['.DS_Store']
        self.src = src
        self.dest = dest
        self.getSrcAndDestFiles()
        self.timedelta = timedelta
        self.check()
        # self.check_command_line_arg()
        self.__remove_ignore_files()

    def errorProcess(self, src, dest):
        if not os.path.exists(src):
            raise StopOperationException("the source folder name is invalid!")

        if not os.path.exists(dest):
            os.makedirs(dest)
            if not self.backend_mode:
                print(
                    'the dest path: {} does not exist, so I create one for you'.
                        format(dest))

        if not os.path.isdir(src) or not os.path.isdir(dest):
            raise StopOperationException(
                "Both 'src' and 'dest' should be folder name!")

    def getSrcAndDestFiles(self):
        self.files_in_dest: list = os.listdir(self.dest)
        self.files_in_src: list = os.listdir(self.src)

    def __run_recursive(self):
        self.files_in_dest: list = os.listdir(self.dest)
        self.files_in_src: list = os.listdir(self.src)
        checktime = datetime.datetime.now()

        for file in self.files_in_src:
            abs_file = os.path.join(self.src, file)
            if not file in self.files_in_dest:
                if not os.path.isdir(abs_file):
                    try:
                        shutil.copy2(abs_file,
                                     os.path.join(self.dest,
                                                  os.path.basename(file)))
                    except shutil.SameFileError:
                        pass
                    Sync_To_Dropbox.num_of_sync_files += 1
                else:
                    inner: Sync_To_Dropbox = Sync_To_Dropbox(
                        abs_file,
                        os.path.join(self.dest, file),
                        timedelta=self.timedelta)
                    inner.__run_recursive()
            else:
                last_create_timedelta = checktime - datetime.datetime.fromtimestamp(
                    os.path.getctime(abs_file))
                last_modify_timedelta = checktime - datetime.datetime.fromtimestamp(
                    os.path.getmtime(abs_file))
                last_change_time = self.which_timedelta_is_later(
                    last_create_timedelta, last_modify_timedelta)

                if last_change_time < self.timedelta:
                    dest_abs_file = os.path.join(self.dest, file)
                    dest_last_create_timedelta = checktime - datetime.datetime.fromtimestamp(
                        os.path.getctime(dest_abs_file))
                    dest_last_modify_timedelta = checktime - datetime.datetime.fromtimestamp(
                        os.path.getmtime(dest_abs_file))
                    dest_last_change_time = self.which_timedelta_is_later(
                        dest_last_create_timedelta, dest_last_modify_timedelta)

                    if dest_last_change_time < last_change_time:
                        if not self.backend_mode:
                            print(
                                "The file '{}' in 'dest' is newer, so I ignore it".
                                    format(os.path.join(self.dest, file)))
                    else:
                        if not os.path.isdir(abs_file):
                            try:
                                shutil.copy2(abs_file,
                                             os.path.join(self.dest,
                                                          os.path.basename(file)))
                            except shutil.SameFileError:
                                pass
                            Sync_To_Dropbox.num_of_sync_files += 1

                        else:
                            inner: Sync_To_Dropbox = Sync_To_Dropbox(
                                abs_file,
                                os.path.join(self.dest, file),
                                timedelta=self.timedelta)
                            inner.__run_recursive()

    def run(self):
        if self.backend_mode:
            while not Sync_To_Dropbox.stop:
                self.__run_recursive()
                time.sleep(Sync_To_Dropbox.run_interval)
        else:
            self.__run_recursive()
            print("Sync Files:  {}".format(Sync_To_Dropbox.num_of_sync_files))
            Sync_To_Dropbox.num_of_sync_files = 0

    def check(self):
        src_folder = self.src.split(os.path.sep)[-1]
        if src_folder in self.files_in_dest:
            if self.backend_mode:
                raise StopOperationException(
                    "The src folder name is the same as the dist folder\nIn backend mode, so I stop"
                )
            res: str = input(
                "The src folder name is the same as the dist folder\ndo you want to continue? (y / n)"
            )
            if res == 'y':
                pass
            elif res == 'n':
                raise StopOperationException("You stopped the operation")
            else:
                raise StopOperationException("Not known operation")

    def check_command_line_arg(self):
        if len(sys.argv) > 2:
            if not self.backend_mode:
                print(
                    "Too many arguments\nShould have 1 argument:  'timedelta'\n"
                    +
                    "e.g.: days=1 / minutes=1 / hours=1 / seconds=1 / weeks=1 "
                )
            else:
                raise StopOperationException(
                    "Too many arguments\nShould have 1 argument:  'timedelta'\n"
                    +
                    "e.g.: days=1 / minutes=1 / hours=1 / seconds=1 / weeks=1 "
                )
            exit(0)

        elif len(sys.argv) == 2:
            temp_timedelta = datetime.timedelta(seconds=0)
            try:
                arg = sys.argv[-1]
                k, v = arg.split('=')
                temp_timedelta = datetime.timedelta(**{k: float(v)})
            except Exception:
                if not self.backend_mode:
                    print(datetime.timedelta.__doc__)

            if not temp_timedelta.seconds == 0:
                self.timedelta = temp_timedelta
        else:
            pass

    def which_timedelta_is_later(self, t1: datetime.timedelta,
                                 t2: datetime.timedelta):
        '''
            timedelta = now - lastmodified
        '''
        if t1 < t2:
            return t1
        else:
            return t2

    def __remove_ignore_files(self):
        for file in self.ignore_files:
            try:
                if '*' in file:  # regular expressoin
                    name, extension = file.split(".")
                    for src_file in self.files_in_src:
                        if name in src_file or extension in src_file:
                            self.files_in_src = filter(
                                lambda file_name: not (
                                        name in file_name or extension in file_name),
                                self.files_in_src)
                else:
                    self.files_in_src.remove(file)
            except Exception:
                pass

    @property
    def ignore(self):
        return self.ignore_files

    @ignore.setter
    def ignore(self, ignore: list):
        self.ignore_files.extend(ignore)
        self.__remove_ignore_files()

    @property
    def srcDir(self):
        return self.src

    @srcDir.setter
    def srcDir(self, val):
        self.errorProcess(val, self.dest)
        self.getSrcAndDestFiles()
        self.check()
        self.__remove_ignore_files()
        self.src = val

    @property
    def destDir(self):
        return self.dest

    @destDir.setter
    def destDir(self, val):
        self.errorProcess(self.src, val)
        self.getSrcAndDestFiles()
        self.check()
        self.__remove_ignore_files()
        self.dest = val


home = os.path.expanduser('~')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("should have 2 parameters")
        print("1: src.  2: dest")
        sys.exit(-1)
    instance = Sync_To_Dropbox(sys.argv[1], sys.argv[2])
    instance.run()
