import os
import imageio

import torch
import torch.utils.data as data

from rcan.data import common

class Images(data.Dataset):
    def __init__(self, args, train=False):
        self.args = args
        self.train = False
        self.name = 'MyImage'
        self.scale = args.scale
        self.idx_scale = 0

        self.filelist = []
        for image in args.images:
            try:
                imageio.imread(image)
                self.filelist.append(image)
            except:
                pass

    def __getitem__(self, idx):
        fullpath = self.filelist[idx]
        dirname = os.path.dirname(fullpath)
        filename = os.path.split(fullpath)[-1]
        filename, extension = os.path.splitext(filename)
        lr = imageio.imread(fullpath)
        lr = common.set_channel([lr], self.args.n_colors)[0]

        return common.np2Tensor([lr], self.args.rgb_range)[0], -1, filename, dirname, extension

    def __len__(self):
        return len(self.filelist)

    def set_scale(self, idx_scale):
        self.idx_scale = idx_scale
