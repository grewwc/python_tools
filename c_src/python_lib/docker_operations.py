import subprocess
from typing import List
import re
from pprint import pprint
import argparse
import colorama
from colorama import Fore
from contextlib import contextmanager
import sys

colorama.init()


@contextmanager
def color(color: str):
    try:
        colorObj = getattr(Fore, color.upper())
        print(colorObj, end='')
        yield
    finally:
        print(Fore.RESET, end='')


class DockerContainer:
    containers = set()

    def __init__(self, container_id, image, command, created, status, ports, names):
        self.container_id = container_id
        self.image = image
        self.command = command
        self.created = created
        self.status = status
        self.ports = ports
        self.names = names
        self.containers.add(self)

    def __repr__(self):
        res = ''
        for i, (k, v) in enumerate(vars(self).items()):
            s = '{}: {}{}{}, '.format(
                k.replace('_', ' ').upper(), Fore.GREEN, v, Fore.RESET)

            if v is None or v.strip() == '':
                continue

            res += s

        res = res.rstrip()[:-1]  # remove the last comma
        return res

    def __eq__(self, other):
        return self.container_id == other.container_id

    def __hash__(self):
        keys = list(vars(self).keys())
        res = hash(getattr(self, keys[0]))

        for key in keys[1:]:
            res ^= hash(getattr(self, key))
        return res

    @classmethod
    def filter_by_image(cls, image: str):
        return [container for container in cls.containers if container.image == image]

    def remove(self) -> bool:
        self.containers.remove(self)
        return CMDUtils.remove_one_container(self)

    def paused(self) -> bool:
        status: str = self.status
        return 'paused' in status.lower()

    @staticmethod
    def stop_all():
        running_containers = CMDUtils.register_all_containers(
            include_stop=False)
        for container in running_containers:
            CMDUtils.stop_one_container(container)


class CMDUtils:
    @staticmethod
    def _subprocess_run(arguments_list: List[str]) -> bool:
        p = subprocess.Popen(arguments_list,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode('utf8').strip()
        err = err.decode('utf8').strip()

        if CMDUtils._has_err(err):
            return False

        print(out)
        return True

    @staticmethod
    def _has_err(err)->bool:
        if err is not None and len(err.strip()) != 0:
            print(err)
            return True
        return False

    @staticmethod
    def register_all_containers(include_stop=True) -> List[DockerContainer]:
        argument_list = ['docker', 'ps']
        if include_stop:
            argument_list.append('-a')

        process = subprocess.Popen(argument_list,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf8").strip()
        stderr = stderr.decode("utf8").strip()

        if CMDUtils._has_err(stderr):
            return

        stdout = stdout.split("\n")
        args_for_all_containers = split_args(stdout)
        return [DockerContainer(*args) for args in args_for_all_containers]

    @staticmethod
    def remove_one_container(container: DockerContainer) -> bool:
        return CMDUtils._subprocess_run(["docker", "rm", "-v", container.container_id])

    @staticmethod
    def stop_one_container(container: DockerContainer) -> bool:
        return CMDUtils._subprocess_run(['docker', 'stop', container.container_id])


def split_args(outputs: List[str]) -> List[List[str]]:
    tab_line = outputs[0]
    table_names = ('CONTAINER ID', 'IMAGE', 'COMMAND',
                   'CREATED', 'STATUS', 'PORTS', 'NAMES')
    table_indices = tuple(tab_line.index(name) for name in table_names)
    table_name_lengths = []
    for i in range(len(table_indices)-1):
        table_name_lengths.append(table_indices[i+1]-table_indices[i])

    res = []
    for args in outputs[1:]:
        args_list = []
        for i, idx in enumerate(table_indices):
            length = table_name_lengths[i] if i + \
                1 < len(table_indices) else len(args)-table_indices[-1]
            args_list.append(
                args[table_indices[i]:table_indices[i]+length].strip())
        res.append(args_list)

    return res


def run():

    CMDUtils.register_all_containers()
    parser = argparse.ArgumentParser()

    parser.add_argument('--rm-container-by-image', '-rmc',
                        help="IMAGE name of docker containers")
    parser.add_argument('--list-paused', action="store_true",
                        help="List all paused containers")
    parser.add_argument('--ignore', action='store_true',
                        help="continue operating when errors occur")
    parser.add_argument('--stop-all', action='store_true',
                        help='Stop all running docker containers')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()

    if args.rm_container_by_image is not None:
        image_name = args.rm_container_by_image
        to_remove = DockerContainer.filter_by_image(image_name)
        for container in to_remove:
            success = container.remove()
            if not success and not args.ignore:
                return

    if args.list_paused:
        for container in DockerContainer.containers:
            if container.paused():
                print(container)

    if args.stop_all:
        DockerContainer.stop_all()


if __name__ == '__main__':
    run()
