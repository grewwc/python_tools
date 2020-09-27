import os
from python_tools.constants.cmd_colors import colors
from python_tools.small_components.terminal import cd

bundle_prefix = os.path.join(os.path.expanduser("~"), ".vim/bundle")
all_paths = []


def add_to_path():
    global all_paths
    relative_paths = os.listdir(bundle_prefix)
    print("{header}All Plugins Found{header}: ".format(header=colors.HEADER),
          relative_paths)
    for p in relative_paths:
        abs_path = os.path.join(bundle_prefix, p)
        if os.path.isdir(abs_path):
            all_paths.append(os.path.join(bundle_prefix, abs_path))


def update():
    for path in all_paths:
        with cd(path):
            print("{header}Updating: {path}{header}"
                  .format(header=colors.OKGREEN, path=path))
            print()
            os.system("git pull")


if __name__ == "__main__":
    add_to_path()
    update()
