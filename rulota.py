#!/usr/bin/python3

import argparse
import subprocess
import os
from shutil import copyfile

DEFINED_ACTIONS = ['deploy', 'halt', 'start', 'destroy']
SOURCE_VM = 'centos'


def deploy(arguments):
    subprocess.run(['vboxmanage', 'clonevm', SOURCE_VM, '--name', arguments.hostname, '--register'])

    os.chdir(os.path.dirname(__file__))
    sf_path = os.getcwd() + "/sf_" + arguments.hostname
    if not os.path.exists(sf_path):
        os.makedirs(sf_path)

    dst = os.path.join(sf_path, 'bootstrap.sh')
    src = os.path.join(os.getcwd(), 'bootstrap.sh')
    config = os.path.join(sf_path, 'config')
    copyfile(src, dst)

    with open(config, 'w') as fout:
        fout.write('IPV4="' + arguments.ipv4 + '"')
        if not os.path.isfile('~/.ssh/id_rsa.pub'):
            subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-f', '~/.ssh/id_rsa', '-N', '""'])

        with open('~/.ssh/id_rsa.pub') as keyfile:
            key = keyfile.read()

        fout.write('SSH_KEY="' + key + '"')

    subprocess.run(['vboxmanage', 'sharedfolder', 'add', arguments.hostname, '--name', 'scripts', '--hostpath', sf_path,
                    '--readonly', '--automount'])


def halt(arguments):
    subprocess.run(['vboxmanage', 'controlvm', arguments.hostname, 'savestate'])


def start(arguments):
    subprocess.run(['vboxmanage', 'startvm', arguments.hostname])


def destroy(arguments):
    subprocess.run(['vboxmanage', 'unregistervm', arguments.hostname, '--delete'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='%(prog)s ' + '[' + '|'.join(DEFINED_ACTIONS) + ']' + ' hostname ' + 'ipv4')
    parser.add_argument('action', type=str, help='action for taget vm: ' + '|'.join(DEFINED_ACTIONS))
    parser.add_argument('hostname', type=str, help='name of the target vm')
    parser.add_argument('ipv4', type=str, help='ip to be assigned to the vm')
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

