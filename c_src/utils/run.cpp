#include "run.h"

struct stat file_state;

string filter_args(int argc, char **argv)
{
    string res = "";
    for (int i = 1; i < argc; i++)
    {
        res += argv[i];
        res += " ";
    }
    return res;
}

void run(int argc, char **argv, string rel_path)
{
    char python_tools[200];
    GetEnvironmentVariableA("PYTHON_TOOLS",
                            python_tools, 200);
    string abs_path = string(python_tools) + rel_path;
    string args = filter_args(argc, argv);
    // std::cout << args << std::endl;
    string cmd = "python \"" + abs_path + "\" " + args;
    system(cmd.c_str());
}

vector<wwcString> listdir(const char *dir)
{
    WIN32_FIND_DATAA found_file;
    vector<wwcString> files;
    wwcString s_dir{dir};
    // get current dir if '.'
    if (s_dir.strip() == ".")
    {
        char buf[200];
        GetCurrentDirectoryA(200, buf);
        s_dir = buf;
    }

    if (!s_dir.endsWith("/*"))
    {
        s_dir += "/*";
    }

    HANDLE handle = FindFirstFileA(s_dir.c_str(), &found_file);
    // cout << "here " << s_dir<<endl;
    if (handle != INVALID_HANDLE_VALUE)
    {
        while (FindNextFileA(handle, &found_file))
        {
            wwcString name = found_file.cFileName;
            if (name != ".." && name != ".")
                files.emplace_back(found_file.cFileName);
        }
    }
    return files;
}

bool is_dir(const char *fname)
{
    wwcString s_fname{fname};
    if (s_fname.endsWith("/*"))
    {
        s_fname = s_fname.split('/')[0];
    }
    stat(s_fname.c_str(), &file_state);
    return file_state.st_mode & S_IFDIR;
}

bool is_file(const char *fname)
{
    stat(fname, &file_state);
    return file_state.st_mode & S_IFREG;
}

bool is_exists(const char *fname)
{
    return stat(fname, &file_state) == 0;
}

time_t get_mtime(const char *fname)
{
    stat(fname, &file_state);
    return file_state.st_mtime;
}

void print_with_attr(const char *msg, WORD wAttributes)
{
    HANDLE handle = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_SCREEN_BUFFER_INFO info;
    GetConsoleScreenBufferInfo(handle, &info);
    bool succeed = SetConsoleTextAttribute(handle, wAttributes);
    if (!succeed)
    {
        cout << "cannot set console text attribute " << __FILE__ << "( "
             << __LINE__ << ")\n";
    }
    cout << msg;
    SetConsoleTextAttribute(handle, info.wAttributes);
}

const size_t get_window_width()
{
    CONSOLE_SCREEN_BUFFER_INFO info;
    GetConsoleScreenBufferInfo(GetStdHandle(STD_OUTPUT_HANDLE), &info);
    return info.dwSize.X;
}