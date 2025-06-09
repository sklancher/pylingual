__all__ = ['TSClassifier', 'TSRegressor', 'TSForecaster']
from fastai.learner import Learner
from fastai.optimizer import Adam
from fastai.metrics import accuracy
from fastai.losses import *
from .imports import *
from .learner import *
from .data.validation import *
from .data.core import *
from .models.InceptionTimePlus import *
from .models.utils import *
from .metrics import *

class TSClassifier(Learner):

    def __init__(self, X, y=None, splits=None, tfms=None, inplace=True, sel_vars=None, sel_steps=None, weights=None, partial_n=None, train_metrics=False, bs=[64, 128], batch_size=None, batch_tfms=None, shuffle_train=True, drop_last=True, num_workers=0, do_setup=True, device=None, arch=None, arch_config={}, pretrained=False, weights_path=None, exclude_head=True, cut=-1, init=None, loss_func=None, opt_func=Adam, lr=0.001, metrics=accuracy, cbs=None, wd=None, wd_bn_bias=False, train_bn=True, moms=(0.95, 0.85, 0.95), path='.', model_dir='models', splitter=trainable_params, verbose=False):
        if splits is None:
            splits = TSSplitter()(X)
        if tfms is None:
            tfms = [None, TSClassification()]
        if batch_size is not None:
            bs = batch_size
        dls = get_ts_dls(X, y=y, splits=splits, sel_vars=sel_vars, sel_steps=sel_steps, tfms=tfms, inplace=inplace, path=path, bs=bs, batch_tfms=batch_tfms, num_workers=num_workers, weights=weights, partial_n=partial_n, device=device, shuffle_train=shuffle_train, drop_last=drop_last)
        if loss_func is None:
            if hasattr(dls, 'loss_func'):
                loss_func = dls.loss_func
            elif hasattr(dls, 'cat') and (not dls.cat):
                loss_func = MSELossFlat()
            elif hasattr(dls, 'train_ds') and hasattr(dls.train_ds, 'loss_func'):
                loss_func = dls.train_ds.loss_func
            else:
                loss_func = CrossEntropyLossFlat()
        if init is True:
            init = nn.init.kaiming_normal_
        if arch is None:
            arch = InceptionTimePlus
        elif isinstance(arch, str):
            arch = get_arch(arch)
        model = build_ts_model(arch, dls=dls, device=device, verbose=verbose, pretrained=pretrained, weights_path=weights_path, exclude_head=exclude_head, cut=cut, init=init, arch_config=arch_config)
        setattr(model, '__name__', arch.__name__)
        try:
            (model[0], model[1])
            splitter = ts_splitter
        except:
            pass
        super().__init__(dls, model, loss_func=loss_func, opt_func=opt_func, lr=lr, cbs=cbs, metrics=metrics, path=path, splitter=splitter, model_dir=model_dir, wd=wd, wd_bn_bias=wd_bn_bias, train_bn=train_bn, moms=moms)
        if train_metrics and hasattr(self, 'recorder'):
            self.recorder.train_metrics = True

class TSRegressor(Learner):

    def __init__(self, X, y=None, splits=None, tfms=None, inplace=True, sel_vars=None, sel_steps=None, weights=None, partial_n=None, train_metrics=False, bs=[64, 128], batch_size=None, batch_tfms=None, shuffle_train=True, drop_last=True, num_workers=0, do_setup=True, device=None, arch=None, arch_config={}, pretrained=False, weights_path=None, exclude_head=True, cut=-1, init=None, loss_func=None, opt_func=Adam, lr=0.001, metrics=None, cbs=None, wd=None, wd_bn_bias=False, train_bn=True, moms=(0.95, 0.85, 0.95), path='.', model_dir='models', splitter=trainable_params, verbose=False):
        if splits is None:
            splits = TSSplitter()(X)
        if tfms is None:
            tfms = [None, TSRegression()]
        if batch_size is not None:
            bs = batch_size
        dls = get_ts_dls(X, y=y, splits=splits, sel_vars=sel_vars, sel_steps=sel_steps, tfms=tfms, inplace=inplace, path=path, bs=bs, batch_tfms=batch_tfms, num_workers=num_workers, weights=weights, partial_n=partial_n, device=device, shuffle_train=shuffle_train, drop_last=drop_last)
        if loss_func is None:
            if hasattr(dls, 'loss_func'):
                loss_func = dls.loss_func
            elif hasattr(dls, 'cat') and (not dls.cat):
                loss_func = MSELossFlat()
            elif hasattr(dls, 'train_ds') and hasattr(dls.train_ds, 'loss_func'):
                loss_func = dls.train_ds.loss_func
            else:
                loss_func = MSELossFlat()
        if init is True:
            init = nn.init.kaiming_normal_
        if arch is None:
            arch = InceptionTimePlus
        elif isinstance(arch, str):
            arch = get_arch(arch)
        model = build_ts_model(arch, dls=dls, device=device, verbose=verbose, pretrained=pretrained, weights_path=weights_path, exclude_head=exclude_head, cut=cut, init=init, arch_config=arch_config)
        setattr(model, '__name__', arch.__name__)
        try:
            (model[0], model[1])
            splitter = ts_splitter
        except:
            pass
        super().__init__(dls, model, loss_func=loss_func, opt_func=opt_func, lr=lr, cbs=cbs, metrics=metrics, path=path, splitter=splitter, model_dir=model_dir, wd=wd, wd_bn_bias=wd_bn_bias, train_bn=train_bn, moms=moms)
        if train_metrics and hasattr(self, 'recorder'):
            self.recorder.train_metrics = True

class TSForecaster(Learner):

    def __init__(self, X, y=None, splits=None, tfms=None, inplace=True, sel_vars=None, sel_steps=None, weights=None, partial_n=None, train_metrics=False, bs=[64, 128], batch_size=None, batch_tfms=None, shuffle_train=True, drop_last=True, num_workers=0, do_setup=True, device=None, arch=None, arch_config={}, pretrained=False, weights_path=None, exclude_head=True, cut=-1, init=None, loss_func=None, opt_func=Adam, lr=0.001, metrics=None, cbs=None, wd=None, wd_bn_bias=False, train_bn=True, moms=(0.95, 0.85, 0.95), path='.', model_dir='models', splitter=trainable_params, verbose=False):
        if splits is None:
            splits = TSSplitter()(X)
        if tfms is None:
            tfms = [None, TSForecasting()]
        if batch_size is not None:
            bs = batch_size
        dls = get_ts_dls(X, y=y, splits=splits, sel_vars=sel_vars, sel_steps=sel_steps, tfms=tfms, inplace=inplace, path=path, bs=bs, batch_tfms=batch_tfms, num_workers=num_workers, weights=weights, partial_n=partial_n, device=device, shuffle_train=shuffle_train, drop_last=drop_last)
        if loss_func is None:
            if hasattr(dls, 'loss_func'):
                loss_func = dls.loss_func
            elif hasattr(dls, 'cat') and (not dls.cat):
                loss_func = MSELossFlat()
            elif hasattr(dls, 'train_ds') and hasattr(dls.train_ds, 'loss_func'):
                loss_func = dls.train_ds.loss_func
            else:
                loss_func = MSELossFlat()
        if init is True:
            init = nn.init.kaiming_normal_
        if arch is None:
            arch = InceptionTimePlus
        elif isinstance(arch, str):
            arch = get_arch(arch)
        model = build_ts_model(arch, dls=dls, device=device, verbose=verbose, pretrained=pretrained, weights_path=weights_path, exclude_head=exclude_head, cut=cut, init=init, arch_config=arch_config)
        setattr(model, '__name__', arch.__name__)
        try:
            (model[0], model[1])
            splitter = ts_splitter
        except:
            pass
        super().__init__(dls, model, loss_func=loss_func, opt_func=opt_func, lr=lr, cbs=cbs, metrics=metrics, path=path, splitter=splitter, model_dir=model_dir, wd=wd, wd_bn_bias=wd_bn_bias, train_bn=train_bn, moms=moms)
        if train_metrics and hasattr(self, 'recorder'):
            self.recorder.train_metrics = True