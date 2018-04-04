#!/usr/bin/python3

import argparse
import subprocess

defined_actions = ['deploy', 'halt', 'start', 'destroy']
source_vm = 'centos'


def deploy(args):
    subprocess.run(['vboxmanage', 'clonevm', source_vm, '--name', args.hostname, '--register'])


def halt(args):
    subprocess.run(['vboxmanage', 'controlvm', args.hostname, 'pause'])


def start(args):
    subprocess.run(['vboxmanage', 'controlvm', args.hostname, 'resume'])


def destroy(args):
    subprocess.run(['vboxmanage', 'unregistervm', args.hostname, '--delete'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    parser.add_argument('action', metavar='1', type=str)
    parser.add_argument('hostname', metavar='1', type=str)

    args = parser.parse_args()

    if args.action not in defined_actions:
        parser.print_help()
        exit(0)

    elif args.action == 'deploy':
        deploy(args)

    elif args.action == 'halt':
        halt(args)

    elif args.action == 'start':
        start(args)

    elif args.action == 'destroy':
        destroy(args)

    print(args)
