import yaml
import os
from argparse import ArgumentParser
import subprocess

HOME = os.environ['HOME']


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--ls', '-ls', type=str, nargs="?", default='ls.default')
    parser.add_argument('--gen', '-gen', type=str, default='')
    return parser


def connect(address):
    cmd = f'ssh {address}'
    if 'address' in address:
        host = address['address']
        private_key = address['private_key']
        cmd = f"ssh -i {private_key} {host}"

    os.system(cmd)


def run():
    server_address_fname = os.path.join(HOME, '.configW', 'server.yaml')

    if not os.path.exists(os.path.dirname(server_address_fname)):
        os.makedirs(os.path.dirname(server_address_fname))

    if not os.path.exists(server_address_fname):
        print(f"{server_address_fname} NOT found")
        return

    with open(server_address_fname) as f:
        servers = yaml.load(f, yaml.BaseLoader)

    parser = parse_args()
    args, unknown = parser.parse_known_args()
    server = unknown[0] if len(unknown) > 0 else None

    if args.ls != 'ls.default':
        # args.ls is set
        keys = servers.keys() if args.ls is None else [args.ls]
        try:
            for key in keys:
                print(f'\t{key}: {servers[key]}')
        except KeyError:
            print(f'{key} not in {list(servers.keys())}')

        return
    if args.gen != '':
        pass

    if server not in servers:
        print(f"'{server}' not found. known: {list(servers.keys())} ($HOME/.configW/server.yaml)")
        return

    connect(servers[server])


if __name__ == '__main__':
    run()
