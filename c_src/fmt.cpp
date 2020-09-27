#include "utils/run.h"
#include <cstdio>

constexpr auto replace_empty_space = [](char ch) {
    return ch == ' ' ? '_' : ch;
};
void replace(wwcString fname)
{
    if (is_file(fname.c_str()) && !fname.contains(" "))
        return;
    auto new_fname = fname.replace_char_fn_copy(replace_empty_space);
    rename(fname.c_str(), new_fname.c_str());

    if (is_dir(fname.c_str()))
    {
        auto subs = listdir(fname.c_str());
        for (auto &sub : subs)
        {
            replace(new_fname + "/" + sub);
        }
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        cout << "invalid argument" << endl;
        exit(1);
    }

    wwcString arg{argv[1]};
    replace(arg);
}