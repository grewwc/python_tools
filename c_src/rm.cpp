#include "utils/run.h"

int main(int argc, char* argv[]){
    string code_path = R"(\c_src\python_lib\rm.py)";
    run(argc, argv, code_path);
}