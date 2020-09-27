#include "utils/run.h"
#include <fstream>
#include <ios>

using namespace std;

void read_file_backward(const char *fpath, const size_t N)
{
    cout << '\n';
    size_t count = 0;
    ifstream reader{fpath};
    if (!reader.is_open())
    {
        cout << "cannot open file " << fpath << endl;
        exit(-1);
    }

    wwcString line;
    wwcString total;
    while (getline(reader, line))
    {
        total += wwcString("  ") + line + '\n';
    }

    auto lines = total.split('\n');
    total.clear();
    long long from = lines.size() - N;
    if (from < 0)
        from = 0;
    for (size_t line_idx = from; line_idx < lines.size(); line_idx++)
    {
        line = lines[line_idx];
        auto wrapped = line.line_wrap(get_window_width() - 4);
        for (int i = 1; i < wrapped.size(); i++)
        {
            wrapped[i] = wwcString("  ") + wrapped[i];
        }
        line = wwcString::join("\n", wrapped);
        total += (line + '\n');
    }

    for(const auto line: total.split('\n')){
        cout << line << "\n";
    }
    cout << '\n';
}

int main(int argc, char *argv[])
{
    size_t num_of_lines = 10ULL;
    if (argc > 3 || argc < 2)
    {
        cout << "invalid argument " << endl;
        cout << "tail -10 file " << endl;
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
    read_file_backward(fpath.c_str(), num_of_lines);
}