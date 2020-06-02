#!/usr/bin/env python3

# Antoine Patel (antoine.patel.fr@gmail.com)
# Simple installation script using a python virtual environment.
# Using venv means it requires python version >= 3.3.

import os, sys, platform
from os.path import normpath, dirname, abspath, isfile
from inspect import getsourcefile
from distutils.spawn import find_executable

repo = dirname(abspath(getsourcefile(lambda:0)))
system = platform.system().lower()

if sys.version_info < (3, 4, 0):
    print(f'[ERROR] this installation script requires python 3.4 or later.')
    print(f'Python version used to run this script: {platform.python_version()}')
    exit(2)

os.chdir(repo)
print(f'Installing in directory: {repo}')

envdir = normpath('./rcan-env')
# Some linux distros have 'python' refers to 'python 2.x', while
# 'python3' refers to the 3.x version. On Windows it's usually not the
# case.
python = 'python3' if find_executable('python3') is not None else 'python'
vcmd = f'{python} -m venv {envdir}'
# Init a python virtual environment if needed.
if not isfile(normpath(f'{envdir}/pyvenv.cfg')):
    print(f'seting up the python virtual environment: {cmd}')
    os.system(vcmd)

if not isfile(normpath(f'{envdir}/pyvenv.cfg')):
    print(f'[error] Failed to create the python virtual environment in {envdir}')
    exit(3)

vpip = None
vpython = None

# Find a binary inside the virtual environment.
def get_vbin(binary):
    candidates = (f'{envdir}/bin/{binary}',
                  f'{envdir}/bin/{binary}3',
                  f'{envdir}/Scripts/{binary}',
                  f'{envdir}/Scripts/{binary}3')
    return next(normpath(x) for x in candidates
         if isfile(normpath(x)))

# The pip binary for the virtual environment.
vpip = get_vbin('pip')
# The python binary for the virtual environment.
vpython = get_vbin('python')

# I had pip not being added to the virtual environment on Windows, not
# sure why. Redoing the venv stuff fix it, again not idea why (don't
# care).
if not vpip:
    os.system(vcmd)
    vpip = get_vbin('pip')

# If still not found, exit...
if not vpip:
    print(f'[error] Failed to find pip in {envdir}')
    exit(4)

# See https://github.com/scikit-image/scikit-image/issues/4673
cmd = f'{vpip} install -U pip'
print(f'Updating pip: {cmd}')
os.system(cmd)

cmd = f'{vpip} install -r requirements.txt'
print(f'Installing dependencies (locally, for this virtual env only): {cmd}')
os.system(cmd)

cmd = f'{vpython} -m torch.utils.collect_env'
print(f'Showing torch infos (incl. CUDA support) about your system: {cmd}')
os.system(cmd)
