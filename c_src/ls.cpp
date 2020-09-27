#include "utils/run.h"
#include <iomanip>
#include <windows.h>



void print_args(vector<wwcString> args, wwcString empty_space = "  ")
{
    const unsigned int WIDTH = get_window_width();
    size_t maxlen = 0;
    for (auto &e : args)
    {
        if (is_dir(e.c_str()))
            e += '/';
        maxlen = std::max<size_t>(maxlen, e.size());
    }
    auto num_each_row = WIDTH / (maxlen + empty_space.size());
    if (num_each_row == 0)
        num_each_row++;
    // begin to print
    for (size_t i = 0; i < args.size(); i++)
    {
        if (i % num_each_row == 0)
        {
            cout << "\n";
        }

        cout << empty_space
             << std::setw(std::min<size_t>(maxlen, WIDTH - empty_space.size() - 1))
             << std::left << args[i];
    }
    cout << endl;
}

int main(int argc, char *argv[])
{
    vector<wwcString> args;
    wwcString empty_space = "    ";
    const unsigned int WIDTH = get_window_width();

    if (argc == 1)
    {
        unsigned int cursor = 0;
        char buf[500];
        GetCurrentDirectoryA(sizeof(buf), buf);
        auto res = listdir(buf);
        print_args(res);
        return 0;
    }
    if (argc == 2)
    {
        wwcString arg{argv[1]};
        if (arg.contains("*"))
        { // nothing to output
            cout << endl;
            return 0;
        }
        if (arg.strip() == ".")
        {
            main(argc - 1, argv);
            return 0;
        }
        if (is_dir(argv[1]))
        {
            cout << empty_space << wwcString(argv[1]).strip('/') << "/" << endl;
            auto res = listdir(argv[1]);
            print_args(res, empty_space * 2);
        }
        else
        {
            if (!is_exists(argv[1]))
            { // don't print anything
                cout << endl;
                return 0;
            }
            cout << empty_space << argv[1] << endl;
        }
        return 0;
    }
    for (int i = 1; i < argc; i++)
    {
        args.emplace_back(argv[i]);
    }
    print_args(args);
}