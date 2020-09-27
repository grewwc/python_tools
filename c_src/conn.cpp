#include "utils/run.h"

int main(int argc, char* argv[]){
    string code_path = R"(\c_src\python_lib\connect_to_server.py)";
    run(argc, argv, code_path);
}

