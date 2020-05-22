#!/usr/bin/env python3

# Antoine Patel (antoine.patel.fr@gmail.com)
# Simple installation script using a python virtual environment.
# Using venv means it requires python version >= 3.3.

from inspect import getsourcefile
import os, sys, platform

repo = os.path.dirname(os.path.abspath(getsourcefile(lambda:0)))
system = platform.system().lower()
path = lambda x: os.path.normpath(x)

if sys.version_info < (3, 3, 0):
    print(f'[ERROR] this installation script requires python 3.3 or later.')
    print(f'Python version used to run this script: {platform.python_version()}')
    exit(2)

os.chdir(repo)
print(f'Installing in directory: {repo}')

# Init a python virtual environment if needed.
if not os.path.isfile(path('./pyvenv.cfg')):
    cmd = 'python -m venv .'
    print(f'seting up the python virtual environment: {cmd}')
    os.system(cmd)

# The python binary from the virtual environment.
vpython = './bin/python'
vpython = vpython if os.path.isfile(vpython) else './bin/python3'
# The pip binary from the virtual environment.
vpip = './bin/pip'
vpip = vpip if os.path.isfile(vpip) else './bin/pip3'

# See https://github.com/scikit-image/scikit-image/issues/4673
cmd = f'{vpip} install -U pip'
print(f'Updating pip: {cmd}')
os.system(cmd)

cmd = f'{vpip} -r requirements.txt'
print(f'Installing dependencies (locally, for this virtual env only): {cmd}')
os.system(cmd)

cmd = f'{vpython} -m torch.utils.collect_env'
print(f'Showing torch infos (incl. CUDA support) about your system: {cmd}')
os.system(cmd)
