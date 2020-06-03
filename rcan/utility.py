from os.path import normpath, dirname, abspath, isdir, isfile
from inspect import getsourcefile
import time

class timer():
    def __init__(self):
        self.acc = 0
        self.tic()

    def tic(self):
        self.t0 = time.time()

    def toc(self):
        return time.time() - self.t0

    def hold(self):
        self.acc += self.toc()

    def release(self):
        ret = self.acc
        self.acc = 0

        return ret

    def reset(self):
        self.acc = 0

def quantize(img, rgb_range):
    pixel_range = 255 / rgb_range
    return img.mul(pixel_range).clamp(0, 255).round().div(pixel_range)

__here = dirname(abspath(getsourcefile(lambda:0)))
rootdir = normpath(f'{__here}/..')

assert isdir(rootdir), f'{rootdir} is expected to be a valid directory'

# Find a binary inside the virtual environment.
def get_vbin(binary):
    envdir = normpath(f'{rootdir}/rcan-env')
    assert isdir(envdir), f'{envdir} is expected to be a valid directory'
    candidates = (f'{envdir}/bin/{binary}3',
                  f'{envdir}/bin/{binary}',
                  f'{envdir}/Scripts/{binary}3.exe',
                  f'{envdir}/Scripts/{binary}.exe')
    return next(
        (normpath(x) for x in candidates if isfile(normpath(x))), None)
