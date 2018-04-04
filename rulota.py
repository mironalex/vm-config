#!/usr/bin/python3

import argparse
import subprocess

defined_actions = ['deploy', 'halt', 'start', 'destroy']
source_vm = 'centos'


def deploy(arguments):
    subprocess.run(['vboxmanage', 'clonevm', source_vm, '--name', arguments.hostname, '--register'])


def halt(arguments):
    subprocess.run(['vboxmanage', 'controlvm', arguments.hostname, 'pause'])


def start(arguments):
    subprocess.run(['vboxmanage', 'controlvm', arguments.hostname, 'resume'])


def destroy(arguments):
    subprocess.run(['vboxmanage', 'unregistervm', arguments.hostname, '--delete'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='%(prog)s ' + '[' + '|'.join(defined_actions) + ']' + ' hostname')
    parser.add_argument('action', type=str)
    parser.add_argument('hostname', type=str)

    args = parser.parse_args()

    if args.action not in defined_actions:
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

