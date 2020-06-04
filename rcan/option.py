import argparse
from rcan.utility import get_vbin, rootdir
from os.path import normpath, isfile
from os import getcwd, access, R_OK


parser = argparse.ArgumentParser(description='RCAN: Image Super-Resolution Using Very Deep Residual Channel Attention Networks (Yulun Zhang, Kunpeng Li, Kai Li, Lichen Wang, Bineng Zhong, Yun Fu)')

parser.add_argument('--debug', action='store_true',
                    help='Enables debug mode')
parser.add_argument('images', type=str, nargs='+',
                    help='The image(s) to upscale')
# Note: except for 3, the rest of the code expects --scale to be a
# power of 2, "NotImplementedError" otherwise.
#
# EDIT: tryed to scale by 16, colors disappeared. I don't think it
# works. Restricting to [2, 3, 4, 8]...
parser.add_argument('--scale', type=int, default=2,
                    choices=([2, 3, 4, 8]),
                    help='super resolution scale / upscaling factor.')
parser.add_argument('--chop', action='store_true',
                    help='enable memory-efficient forward')
parser.add_argument('--ignore_invalid_files', action='store_true',
                    help='Ignore invalid images (file not found, unreadable, ...) instead of halting.')
parser.add_argument('--outdir', type=str,
                    help='An optional directory where all results (upscaled images) will be written. Use "." to save in the current directory. If --outdir is left empty, the upscaled images are saved next to their originals (with an added suffix)')

# Hardware specifications
parser.add_argument('--n_threads', type=int, default=3,
                    help='number of threads for data loading')
parser.add_argument('--cpu', action='store_true',
                    help='Use cpu only (no CUDA)')
parser.add_argument('--n_GPUs', type=int, default=1,
                    help='number of GPUs')
parser.add_argument('--seed', type=int, default=1,
                    help='random seed')

# New options
parser.add_argument('--n_resgroups', type=int, default=10,
                    help='number of residual groups')
parser.add_argument('--reduction', type=int, default=16,
                    help='number of feature maps reduction')

# Data specifications
parser.add_argument('--patch_size', type=int, default=192,
                    help='output patch size')
parser.add_argument('--rgb_range', type=int, default=255,
                    help='maximum value of RGB')
parser.add_argument('--n_colors', type=int, default=3,
                    help='number of color channels to use')

# Model specifications
parser.add_argument('--pre_trained_file', type=str,
                    help='The full path to a custom pre-trained model. If empty, one of the following model is choosen according to --scale (best match): RCAN_BIX2.pt, RCAN_BIX3.pt, RCAN_BIX4.pt, RCAN_BIX8.pt. If empty and --scale > 8, RCAN_BIX8.pt is used')
parser.add_argument('--n_resblocks', type=int, default=20,
                    help='number of residual blocks')
parser.add_argument('--n_feats', type=int, default=64,
                    help='number of feature maps')
parser.add_argument('--res_scale', type=float, default=1,
                    help='residual scaling')
parser.add_argument('--precision', type=str, default='single',
                    choices=('single', 'half'),
                    help='FP precision for test (single | half)')
parser.add_argument('--self_ensemble', action='store_true',
                    help='use self-ensemble method for test')

# Optimization specifications
parser.add_argument('--lr', type=float, default=1e-4,
                    help='learning rate')
parser.add_argument('--lr_decay', type=int, default=200,
                    help='learning rate decay per N epochs')
parser.add_argument('--decay_type', type=str, default='step',
                    help='learning rate decay type')
parser.add_argument('--gamma', type=float, default=0.5,
                    help='learning rate decay factor for step decay')
parser.add_argument('--optimizer', default='ADAM',
                    choices=('SGD', 'ADAM', 'RMSprop'),
                    help='optimizer to use (SGD | ADAM | RMSprop)')
parser.add_argument('--momentum', type=float, default=0.9,
                    help='SGD momentum')
parser.add_argument('--beta1', type=float, default=0.9,
                    help='ADAM beta1')
parser.add_argument('--beta2', type=float, default=0.999,
                    help='ADAM beta2')
parser.add_argument('--epsilon', type=float, default=1e-8,
                    help='ADAM epsilon for numerical stability')
parser.add_argument('--weight_decay', type=float, default=0,
                    help='weight decay')

args = parser.parse_args()

# Autoload a model in ../data/model according to given --scale if
# needed.
if args.pre_trained_file is None:
    args.pre_trained_file = normpath(
        f'{rootdir}/data/model/RCAN_BIX{args.scale}.pt')

# Seems like the original code allowed to upscale by multiple factors
# in one invocation, but... the same pre-trained file would be used.
# Also doesn't play nice with the "autoload best matching pre-trained
# file for the --scale" that I added. Not sure if multiple scales for
# the same pre-trained file could ever be useful anyway.
#
# So I dropped the feature, but args.scale still needs to be a list in
# order to play nice with the rest of the code.
args.scale = [args.scale]

args.model = 'RCAN'

checkfile_ok = lambda x: isfile(x) and access(x, R_OK)
if not checkfile_ok(args.pre_trained_file):
    print('Pre-trained file {args.pre_trained_file} not found/unreadable.')
    print('Cannot process images, exiting.')
    exit(3)

bad_files = [i for i in args.images if not checkfile_ok(i)]
print('Some files were not found or unreadable:')
for i in bad_files:
    print(i)
print('')

if args.ignore_invalid_files:
    args.images[:] = [i for i in args.images if i not in bad_files]
else:
    # type=argparse.filetype('r') would cause a serialization error on
    # Windows, something about multiprocessing. Easier to drop it and
    # check for invalid files here.
    print('--ignore_invalid_files is False: exiting.')
    exit(1)

if not len(args.images):
    print('No valid images to process.')
    print('Exiting.')
    exit(2)
else:
    print('Bad files ignored.')

# Handles --outdir='.' on Windows cmd.exe as a convenience.
args.outdir = args.outdir.replace("'", "")
if args.outdir == '.':
    args.outdir = getcwd()

for arg in vars(args):
    if vars(args)[arg] == 'True':
        vars(args)[arg] = True
    elif vars(args)[arg] == 'False':
        vars(args)[arg] = False
