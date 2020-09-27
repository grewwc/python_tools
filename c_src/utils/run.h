#include <windows.h>
#include <string>
#include <iostream>
#include <vector>
#include "wwcString.h"
#include <sys/stat.h>

using std::string;
using std::vector;

using std::endl;
using std::cout;

extern struct stat file_state;

void run(int argc, char **argv, string rel_path);

vector<wwcString> listdir(const char* path);

time_t get_mtime(const char *fname);

bool is_dir(const char* fname);

bool is_file(const char* fname);

bool is_exists(const char* fname);

void print_with_attr(const char* msg, WORD wAttributes);

const size_t get_window_width();
