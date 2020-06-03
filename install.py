#!/usr/bin/env python3

# Antoine Patel (antoine.patel.fr@gmail.com)
# Simple installation script using a python virtual environment.
# Using venv means it requires python version >= 3.3.

import os, sys, platform
from os.path import normpath, dirname, abspath, isfile
from inspect import getsourcefile
from distutils.spawn import find_executable

from rcan.utility import get_vbin, rootdir

repo = dirname(abspath(getsourcefile(lambda:0)))
system = platform.system().lower()

if sys.version_info < (3, 4, 0):
    print(f'[ERROR] this installation script requires python 3.4 or later.')
    print(f'Python version used to run this script: {platform.python_version()}')
    exit(2)

os.chdir(repo)
print(f'Installing in directory: {repo}')

envdir = normpath(f'{rootdir}/rcan-env')
# Some linux distros have 'python' refers to 'python 2.x', while
# 'python3' refers to the 3.x version. On Windows it's usually not the
# case.
python = 'python3' if find_executable('python3') is not None else 'python'

vcmd = f'{python} -m venv {envdir}'
# Init a python virtual environment if needed.
if not isfile(normpath(f'{envdir}/pyvenv.cfg')):
    print(f'seting up the python virtual environment: {vcmd}')
    os.system(vcmd)

if not isfile(normpath(f'{envdir}/pyvenv.cfg')):
    print(f'[error] Failed to create the python virtual environment in {envdir}')
    exit(3)

vpython = None

# The python binary for the virtual environment.
vpython = get_vbin('python')

# See https://github.com/scikit-image/scikit-image/issues/4673
cmd = f'{vpython} -m pip install --upgrade pip'
print(f'Updating pip: {cmd}')
os.system(cmd)

cmd = f'{vpython} -m pip install wheel'
print(f'Installing "wheel": {cmd}')
os.system(cmd)

cmd = f'{vpython} -m pip install -r requirements.txt'
print(f'Installing dependencies (locally, for this virtual env only): {cmd}')
os.system(cmd)

cmd = f'{vpython} -m torch.utils.collect_env'
print(f'Showing torch infos (incl. CUDA support) about your system: {cmd}')
os.system(cmd)
