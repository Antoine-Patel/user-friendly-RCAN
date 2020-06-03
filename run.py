import sys
from os import system
from os.path import normpath

from rcan.utility import get_vbin, rootdir


# Allow to invoke RCAN without having to activate the virtual
# environment or explicitely use the python interpreter of the virtual
# environment.
if __name__ == '__main__':

    # Use the python interpreter inside the virtual environment.
    vpython = get_vbin('python')
    run_script = normpath(f'{rootdir}/_run.py')
    system(f'{vpython} {run_script} {" ".join(sys.argv[1:])}')
