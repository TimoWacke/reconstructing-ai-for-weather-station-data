import torch

from .hole_loss import HoleLoss
#from hole_loss import HoleLoss
from .valid_loss import ValidLoss
from .var_loss import VarLoss
from .fft_loss import FTLoss
from .inpainting_loss import InpaintingLoss

from ..utils.featurizer import VGG16FeatureExtractor
from .. import config as cfg


class ModularizedFunction(torch.nn.Module):
    def __init__(self, forward_op):
        super().__init__()
        self.forward_op = forward_op

    def forward(self, *args, **kwargs):
        return self.forward_op(*args, **kwargs)


class CriterionParallel(torch.nn.Module):
    def __init__(self, criterion):
        super().__init__()
        if not isinstance(criterion, torch.nn.Module):
            criterion = ModularizedFunction(criterion)
        self.criterion = torch.nn.DataParallel(criterion)

    def forward(self, *args, **kwargs):
        multi_dict = self.criterion(*args, **kwargs)
        for key in multi_dict.keys():
            multi_dict[key] = multi_dict[key].mean()
        return multi_dict


def get_loss(img_mask, loss_mask, output, gt, writer, iter_index, setname):

    if cfg.lambda_dict['prc']>0 or cfg.lambda_dict['style']>0:
        criterion = InpaintingLoss(VGG16FeatureExtractor()).to(cfg.device)
    elif cfg.lambda_dict['hole']>0:
        criterion = HoleLoss().to(cfg.device)
    elif cfg.lambda_dict['valid']>0:
        criterion = ValidLoss().to(cfg.device)

    if cfg.multi_gpus:
        loss_func = CriterionParallel(criterion)
    else:
        loss_func = criterion

    mask = img_mask[:, cfg.recurrent_steps, cfg.gt_channels, :, :]
    if loss_mask is not None:
        mask += loss_mask
        assert ((mask == 0) | (mask == 1)).all(), "Not all values in mask are zeros or ones!"

    loss_dict = loss_func(mask, output[:, cfg.recurrent_steps, :, :, :],
                          gt[:, cfg.recurrent_steps, cfg.gt_channels, :, :])

    losses = {"total": 0.0}
    for key, loss in loss_dict.items():
        value = loss * cfg.lambda_dict[key]
        losses[key] = value
        losses["total"] += value

    if cfg.log_interval and iter_index % cfg.log_interval == 0:
        for key in losses.keys():
            writer.add_scalar('loss_{:s}-{:s}'.format(setname, key), losses[key], iter_index)

    return losses["total"]
