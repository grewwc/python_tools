import os
from subprocess import Popen, PIPE
import glob
import pickle

from datetime import datetime, timedelta

last_compile_info_file = "./info/compile_info"


def no_change_since_last_compile(file: str):
    if not os.path.exists(last_compile_info_file):
        return False
    with open(last_compile_info_file, 'rb') as f:
        last_compile_time = pickle.load(f)
    m_time = datetime.fromtimestamp(os.path.getmtime(file))
    return m_time < last_compile_time


def get_c_cpp_file():
    return glob.glob("*.cpp") + glob.glob("*.c")


def get_python_tools_dir():
    try:
        python_tools = os.environ['PYTHON_TOOLS']
        return python_tools
    except KeyError:
        print('"PYTHON_TOOLS" is not set!')
        exit(1)


def compile_source():
    # libtools_path = "C:/Users/grewang/cpp-utils/lib/"
    # libtools_path = "../../lib/"
    libtools_path = "./utils"
    compile_cmd = ["g++", "-O3", "-std=c++17"]
    compile_link = [f"-L{libtools_path}", "-ltools"]
    source_files = get_c_cpp_file()   
    source_without_ext = [f.split('.')[0] for f in source_files]
    bin_files = [f + '.exe' for f in source_without_ext]
    tools_home = get_python_tools_dir()
    bin_dir = os.path.join(tools_home, "bin")

    for i, source_file in enumerate(source_files):
        if not no_change_since_last_compile(source_file) \
                or not no_change_since_last_compile("utils/run.cpp") \
                or not os.path.exists(os.path.join(bin_dir, bin_files[i])):
            outpath = os.path.join(bin_dir, bin_files[i])
            cmd_list = [*compile_cmd, f"{source_file}",
                        "utils/run.cpp"] + compile_link + ["-o", f"{outpath}"]
            print(*cmd_list)
            p = Popen(cmd_list, stdin=PIPE, stdout=PIPE,
                      stderr=PIPE, bufsize=1)
            out, err = p.communicate()
            if out != b'':
                print(out.decode('utf8'))
            if err != b'':
                print(err.decode('utf8'))

    with open(last_compile_info_file, 'wb') as f:
        pickle.dump(datetime.now(), f)


if __name__ == '__main__':
    compile_source()
