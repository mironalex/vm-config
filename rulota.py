#!/usr/bin/python3

import argparse
import subprocess
import os

DEFINED_ACTIONS = ['deploy', 'halt', 'start', 'destroy']
SOURCE_VM = 'centos'


def deploy(arguments):
    subprocess.run(['vboxmanage', 'clonevm', SOURCE_VM, '--name', arguments.hostname, '--register'])

    os.chdir(os.path.dirname(__file__))
    sf_path = os.getcwd() + "/sf_" + arguments.hostname
    if not os.path.exists(sf_path):
        os.makedirs(sf_path)
    subprocess.run(['vboxmanage', 'sharedfolder', 'add', arguments.hostname, '--name', 'scripts', '--hostpath', sf_path,
                    '--readonly', '--automount'])


def halt(arguments):
    subprocess.run(['vboxmanage', 'controlvm', arguments.hostname, 'savestate'])


def start(arguments):
    subprocess.run(['vboxmanage', 'startvm', arguments.hostname])


def destroy(arguments):
    subprocess.run(['vboxmanage', 'unregistervm', arguments.hostname, '--delete'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='%(prog)s ' + '[' + '|'.join(DEFINED_ACTIONS) + ']' + ' hostname')
    parser.add_argument('action', type=str, help='action for taget vm: ' + '|'.join(DEFINED_ACTIONS))
    parser.add_argument('hostname', type=str, help='name of the target vm')
    parser.add_argument('--source', type=str, help='name of the vm to be cloned, default is centos')

    args = parser.parse_args()

    if args.action not in DEFINED_ACTIONS:
        parser.print_usage()
        exit(0)

    elif args.action == 'deploy':
        deploy(args)

    elif args.action == 'halt':
        halt(args)

    elif args.action == 'start':
        start(args)

    elif args.action == 'destroy':
        destroy(args)

