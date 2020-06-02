from rcan.dataloader import MSDataLoader
from rcan.data.images import Images
from torch.utils.data.dataloader import default_collate

class Data:
    def __init__(self, args):
        kwargs = {}
        if not args.cpu:
            kwargs['collate_fn'] = default_collate
            kwargs['pin_memory'] = True
        else:
            kwargs['collate_fn'] = default_collate
            kwargs['pin_memory'] = False

        self.loader_train = None

        images = Images(args, train=False)

        self.loader_test = MSDataLoader(
            args,
            images,
            batch_size=1,
            shuffle=False,
            **kwargs
        )
