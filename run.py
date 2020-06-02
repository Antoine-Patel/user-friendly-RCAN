import sys
from os import system
from os.path import normpath, dirname, abspath
from inspect import getsourcefile


# Allow to invoke RCAN without having to activate the virtual
# environment or explicitely use the python interpreter of the virtual
# environment.
if __name__ == '__main__':

    here = dirname(abspath(getsourcefile(lambda:0)))
    # Use the python interpreter inside the virtual environment.
    vpython = normpath(f'{here}/rcan-env/bin/python')
    run_script = normpath(f'{here}/_run.py')
    system(f'{vpython} {run_script} {" ".join(sys.argv[1:])}')
