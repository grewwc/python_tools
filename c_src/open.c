#include <stdlib.h>
#include <windows.h>
#include <string.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    char fPath[200];
    char *open_path = NULL;

    if (argc == 1)
    {
        open_path = ".";
    }
    else if (argc == 2)
    {
        open_path = argv[1];
    }
    else
    {
        perror("too many arguments\n");
        exit(-1);
    }
    const char *rel_path = "\\small_components\\terminal_open.py";
    GetEnvironmentVariable("PYTHON_TOOLS", fPath, sizeof(fPath));
    strcat(fPath, rel_path);
    char cmd[300] = "python \"";
    strcat(cmd, fPath);
    strcat(cmd, "\" ");
    strcat(cmd, open_path);
    system(cmd);
    return 0;
}