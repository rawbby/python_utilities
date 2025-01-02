#!/bin/python3

from file_lock import FileLock
from run import run

import glob
import os
import sys
from os.path import join, abspath, exists

__all__ = ['ensure_venv']


def lock_venv(cwd):
    os.makedirs(join(cwd, '.venv'), exist_ok=True)
    return FileLock(join(cwd, '.venv', 'venv.lock'))


def ensure_venv(cwd=None, packages=None):
    cwd = abspath(cwd if cwd is not None else os.getcwd())
    packages = packages if packages is not None else []

    if os.name == 'nt':
        venv_executable = join(cwd, '.venv', 'Scripts', 'python.exe')
    else:
        venv_executable = join(cwd, '.venv', 'bin', 'python')

    with lock_venv(cwd):
        if not exists(venv_executable):
            run([sys.executable, '-m', 'venv', '.venv'], cwd=cwd)
            run([venv_executable, '-m', 'pip', 'install', '--upgrade', 'pip'])

        upgrade_packages = []
        site_package_dir = glob.glob(join(cwd, '.venv', 'lib', 'python*', 'site-packages'))[0]
        for package in packages:
            if not exists(join(site_package_dir, package)):
                upgrade_packages.append(package)

        if len(upgrade_packages) > 0:
            run([venv_executable, '-m', 'pip', 'install', '--upgrade', 'pip'] + upgrade_packages)

    if sys.executable != venv_executable:
        run([venv_executable, __file__] + sys.argv[1:])
        sys.exit()


if __name__ == '__main__':
    ensure_venv(packages=sys.argv[1:])
