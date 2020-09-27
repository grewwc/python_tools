#include "utils/run.h"
#include <fstream>
using namespace std;

void read_file(const char *fpath, const size_t num_of_lines)
{
    cout << '\n';
    ifstream reader{fpath};
    wwcString res;
    if (!reader.is_open())
    {
        cout << "cannot open file " << fpath << endl;
        exit(-1);
    }
    wwcString line;
    size_t count = 0ULL;
    while (getline(reader, line) && count < num_of_lines)
    {
        count++;
        auto wrapped = ((wwcString)((wwcString{" "} * 2) + move(line)))
                           .line_wrap(get_window_width() - 4);
        for (int i = 1; i < wrapped.size(); i++)
        {
            wrapped[i] = (wwcString{"  "} + wrapped[i]);
        }
        res += wwcString::join("\n", wrapped) + '\n';
    }
    for (const auto line : res.split('\n'))
    {
        cout << line << "\n";
    }
    cout << "\n";
}

int main(int argc, char *argv[])
{
    size_t num_of_lines = 10ULL;
    if (argc > 3 || argc < 2)
    {
        cout << "invalid argument " << endl;
        cout << "head -10 file " << endl;
        exit(-1);
    }
    wwcString fpath;
    if (argc > 2)
    {
        num_of_lines = wwcString(argv[1]).strip('-').to_long();
        fpath = argv[2];
    }
    else
    {
        fpath = argv[1];
    }
    read_file(fpath.c_str(), num_of_lines);
}