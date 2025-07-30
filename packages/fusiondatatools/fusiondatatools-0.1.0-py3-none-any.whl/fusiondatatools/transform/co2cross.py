import numpy as np

import torch
import torch.nn.functional as F
import torchvision.transforms as VT

from scipy.signal import butter, filtfilt

import copy

from specseg import helpers
from specseg.core.dataset import Transform

class TestTransform(Transform):

    def __init__(self, cfg):
        super().__init__(cfg)
        self.cfg = cfg
        
    def config(self, sample):
        pass
        
    def transform(self, x):
        return x


class HFFeature(Transform):
    
    def __init__(self, cfg):
        super().__init__(cfg)
        self.cfg = copy.deepcopy(cfg)
        self.setup()
        
    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("window", None)
        state.pop("gaussian", None)
        state.pop("butter_b", None)
        state.pop("butter_a", None)
        state.pop("resize", None)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.setup()
        
    def setup(self):
        self.window = torch.hann_window(self.cfg["win_length"])
        self.gaussian = VT.GaussianBlur(
            kernel_size=(self.cfg['kernel_gauss'], self.cfg['kernel_gauss']),
            sigma=(self.cfg['sigma_gauss'], self.cfg['sigma_gauss']))
        self.butter_b, self.butter_a = butter(
                self.cfg['order'], 
                self.cfg['cutoff_frequency'], 
                btype='highpass')
        self.image_size = 518
        self.resize = VT.Resize(
            size=(self.image_size, self.image_size),
            interpolation=VT.InterpolationMode.BICUBIC,
            )
        
    def config(self, sample):
        pass
        
    def transform(self, x):
        x = self._stationarize(x)
        x = self._stft(x)
        x = self._normalize(x)
        x = self._separate(x)
        mean = x.mean(dim=(1,2))
        std = x.std(dim=(1,2))
        x = (x - mean[:,None,None]) / std[:,None,None]
        x = self.resize(x)
        return x
    
    def _stationarize(self, x):
        x = x.numpy()
        x = np.nan_to_num(x)
        for idx in range(x.shape[0]):
            x[idx] = filtfilt(self.butter_b, self.butter_a, x[idx]).copy()
        x = torch.from_numpy(x)
        return x
    
    def _stft(self, x):
        x = torch.stft(
            x,
            n_fft=self.cfg['nfft'],
            hop_length = self.cfg['hop_length'],
            win_length=self.cfg['win_length'],
            window=self.window,
            center=True,
            pad_mode='reflect',
            normalized=False,
            onesided=True,
            return_complex=True
            )
        
        y = torch.zeros(
            (x.shape[0]-1, x.shape[1], x.shape[2]),
            dtype=torch.complex64,
            device=x.device
        )
        
        for i in range(1, x.shape[0]):
            y[i-1] = x[0] * torch.conj(x[i])
        return torch.log(torch.abs(y))
    
    def clamp_quantile(self, x, q=0.997):
        # x: (C, M, N)
        C, M, N = x.shape
        
        # 1) flatten spatial dims -> (C, M*N)
        x_flat = x.reshape(C, -1)
        
        # 2) compute upper/lower per-channel quantiles along dim=1
        upper_q = torch.quantile(x_flat, q,   dim=1)  # shape: (C,)
        lower_q = torch.quantile(x_flat, 1-q, dim=1)  # shape: (C,)
        
        # 3) clamp, broadcasting quantiles back to (C, M, N)
        x_clamped = torch.clamp(
            x,
            min=lower_q[:, None, None],
            max=upper_q[:, None, None],
        )
        return x_clamped
    
    def _normalize(self, x):
        x = self.clamp_quantile(x, q=1-self.cfg['percent_threshold'])
        x = (x - x.mean(dim=-2, keepdim=True)) / (x.std(dim=-2, keepdim=True)  + 1e-6)
        x = (x - x.mean(dim=-1, keepdim=True)) / (x.std(dim=-1, keepdim=True) + 1e-6)
        return x
    
    def _separate(self, x):
        C, M, N = x.shape
        x = self.gaussian(x)
        x = x.reshape(C, -1)
        T = torch.quantile(x, 0.997, dim=1)
        x = x.reshape(C, M, N)
        x = torch.sigmoid(x - T[:, None, None])
        return x
    
    
class HFLabel(Transform):
    
    def __init__(self, cfg):
        super().__init__(cfg)
        self.cfg = copy.deepcopy(cfg)
        
    def config(self, sample):
        features = sample['features']
        self.cfg['nframes'] = features[0].shape[-1]
        
    def transform(self, x):
        x = x.float()
        x = self._interpolate(x)
        return x
    
    def _interpolate(self, x):
        x = x.unsqueeze(0).unsqueeze(0)
        x = F.interpolate(
            x, 
            size=(x.shape[-2], self.cfg['nframes']), 
            mode='nearest', 
            )
        return x.squeeze(0).squeeze(0)