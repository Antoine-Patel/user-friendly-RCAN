import os
import math
from decimal import Decimal

import imageio
import torch
from torch.autograd import Variable
from tqdm import tqdm

from rcan.utility import timer, quantize

class Worker():
    def __init__(self, args, loader, my_model, my_loss):
        self.args = args
        self.scale = args.scale

        self.loader_test = loader.loader_test
        self.model = my_model
        self.loss = my_loss

        self.error_last = 1e8


    def save_result(self, upscaled, scale, path, ofilename, ext):
        sep = '-'
        for candidate in (' ', '_'):
            sep = candidate if candidate in ofilename else sep

        flavor = 'RCANplus' if self.args.self_ensemble else 'RCAN'
        filename = f'{ofilename}{sep}{flavor}{sep}x{scale}'
        fullpath = os.path.normpath(f'{path}/{filename}{ext}')
        normalized = upscaled[0].data.mul(255 / self.args.rgb_range)
        ndarr = normalized.byte().permute(1, 2, 0).cpu().numpy()
        imageio.imsave(fullpath, ndarr)

        return fullpath


    def upscale(self):
        saveds = []
        self.model.eval()

        timer_test = timer()
        with torch.no_grad():
            for idx_scale, scale in enumerate(self.scale):
                self.loader_test.dataset.set_scale(idx_scale)
                tqdm_test = tqdm(self.loader_test, ncols=80)
                for idx_img, (lr, hr, filename, path, ext, _) in enumerate(tqdm_test):
                    filename = filename[0]
                    path = self.args.outdir if self.args.outdir else path[0]
                    ext = ext[0]

                    no_eval = (hr.nelement() == 1)
                    if not no_eval:
                        lr, hr = self.prepare([lr, hr])
                    else:
                        lr = self.prepare([lr])[0]

                    sr = None
                    sr = self.model(lr, idx_scale)
                    sr = quantize(sr, self.args.rgb_range)

                    saveds.append(
                        self.save_result(sr, scale, path, filename, ext))

        print('Saved result{}:'.format('s' if len(saveds) > 1 else ''))
        for f in saveds:
            print(f)

    def prepare(self, l, volatile=False):
        device = torch.device('cpu' if self.args.cpu else 'cuda')
        def _prepare(tensor):
            if self.args.precision == 'half': tensor = tensor.half()
            return tensor.to(device)

        return [_prepare(_l) for _l in l]
