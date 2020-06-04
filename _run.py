# Display --help fast if possible, avoid loading torch etc...
from rcan.option import args, check_args

import torch
from rcan.data import Data
from rcan.model import Model
from rcan.worker import Worker

if __name__ == '__main__':

    check_args(args)
    torch.manual_seed(args.seed)

    loader = Data(args)
    model = Model(args)
    loss = None

    worker = Worker(args, loader, model, loss)
    worker.upscale()
