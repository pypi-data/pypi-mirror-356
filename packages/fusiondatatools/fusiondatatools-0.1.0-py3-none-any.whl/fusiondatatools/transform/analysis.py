import numpy as np
import torch
import torch.nn.functional as F
import torchaudio.functional as AF
import torchvision.transforms as VT
import cv2

from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt2d

from noisereduce.torchgate import TorchGate as TG

from specseg import helpers
from specseg.core.transform import SignalAnalysisTransform

class BaseCase(SignalAnalysisTransform):
    
    def __init__(self, cfg):
        super().__init__(cfg)
        self.window = torch.hann_window(
            self.cfg['win_length'], periodic=True)
        
    def config(self, sample):
        features = sample
        self.cfg['nframes'] = features.shape[1]
        
    def transform_feature(self, x):
        x = self._ensure_dimensions(x)
        x = self._preemphasis(x)
        x = self._stft(x)
        x = self._clamp(x)
        x = self._squeeze(x)
        return x
    
    def _ensure_dimensions(self, x):
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
        if len(x.shape) == 2:
            pass
        return x
    
    def _preemphasis(self, x):
        x = AF.preemphasis(x, 0.97)
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
        return torch.log(torch.abs(x))
    
    def _clamp(self, x):
        vmin = torch.quantile(x.flatten(1), 0.05, dim=1)
        vmax = torch.quantile(x.flatten(1), 0.95, dim=1)
        for i in range(x.shape[0]):
            x[i] = torch.clamp(x[i], vmin[i], vmax[i])
        return x
    
    def _squeeze(self, x):
        x = x.squeeze(0)
        return x
    
class C02N2V(SignalAnalysisTransform):
    
    def __init__(self, cfg):
        super().__init__(cfg)
        self.window = torch.blackman_window(
            self.cfg['win_length'], periodic=True)
        self.resize = VT.Resize(
            size=(512, 512), 
            interpolation=VT.InterpolationMode.BILINEAR
            )
        self.clahe = cv2.createCLAHE(
            clipLimit=48.0, 
            tileGridSize=(8, 8)
            )
        self.tg = TG(sr=500, time_mask_smooth_ms=1024, nonstationary=True)
        
    def config(self, sample):
        features = sample
        self.cfg['nframes'] = features.shape[1]
        
    def transform_feature(self, x):
        x = self._ensure_dimensions(x)
        x = self._preemphasis(x)
        # x = self.tg(x)
        x = self._stft(x)
        x = self._resize(x)
        x = self._normalize(x)
        # xmax = x.max()#torch.quantile(x, 0.95)
        # avmax = (xmax + x.median())/2
        # xstd = x[x < avmax].std()
        # x[x < avmax] = x[x < avmax] * torch.exp(-2*(avmax  - x[x < avmax])**2/xstd**2)
        # x = self._clahe(x)
        x = self._squeeze(x)
        x = self._interpolate(x)
        return x
    
    def _ensure_dimensions(self, x):
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
        if len(x.shape) == 2:
            pass
        return x
    
    def _preemphasis(self, x):
        x = AF.preemphasis(x, 0.97)
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
        return torch.log(torch.abs(x))
    
    def _resize(self, x):
        x = x[:,3:-2]
        # x = self.resize(x)
        return x
    
    def _normalize(self, x):
        x = torch.clamp(x, -7.612810152029919, -1.0128101520299189)
        x = (x - (-7.612810152029919)) / (-1.0128101520299189 - (-7.612810152029919)) * 255
        # x = (x - x.min()) / (x.max() - x.min()) * 255
        return x
    
    def _clahe(self, x):
        x = x.numpy().astype(np.uint8)
        for i in range(x.shape[0]):
            x[i] = self.clahe.apply(x[i])
            x[i] = cv2.medianBlur(x[i], 3)
        x = torch.from_numpy(x).float()
        return x
    
    def _squeeze(self, x):
        x = x.squeeze(0)
        return x
    
    def _interpolate(self, x):
        x = x.unsqueeze(0).unsqueeze(0)
        x = F.interpolate(
            x, 
            size=(244, 244), 
            mode='bicubic', 
            align_corners=False
            )
        return x.squeeze(0).squeeze(0)
    

class Binary1(SignalAnalysisTransform):
    
    def __init__(self, cfg):
        super().__init__(cfg)
        self.window = torch.hann_window(
            self.cfg['win_length'], periodic=True)
        self.resize = VT.Resize(
            size=(512, 512), 
            interpolation=VT.InterpolationMode.BILINEAR
            )
        self.clahe = cv2.createCLAHE(
            clipLimit=48.0, 
            tileGridSize=(8, 8)
            )
        # self.tg = TG(sr=500, time_mask_smooth_ms=1024, nonstationary=True)
        self.border = (25, 25)
        self.pad = VT.Pad(
            padding=(self.border[0], self.border[1], self.border[0], self.border[1]),
            fill=0,
            padding_mode='reflect'
            )
        
    def reset(self):
        self.__init__(self.cfg)
        
    def config(self, sample):
        features = sample
        self.cfg['nframes'] = features.shape[1]
        
    def transform_feature(self, x):
        x = self._ensure_dimensions(x)
        x = self._preemphasis(x)
        x = self._stft(x)
        x = self._clip_extremes(x)
        x = self._clahe(x)
        x[:,0:10] = 0
        x[:,-10:-1] = 0
        x = self._filters(x)
        # x = self._mophology(x)
        x = self._squeeze(x)
        # x = self._interpolate(x)
        return x
    
    def _ensure_dimensions(self, x):
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
        if len(x.shape) == 2:
            pass
        return x
    
    def _preemphasis(self, x):
        x = AF.preemphasis(x, 0.97)
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
        return torch.log(torch.abs(x))
    
    def _expand_border(self, x):
        x = self.pad(x)
        return x
        
    def _clip_extremes(self, x):
        vmin = torch.quantile(x, 0.05)
        vmax = torch.quantile(x, 0.95)
        x = torch.clamp(x, vmin, vmax)
        x = helpers.minmax(x)
        return x
        
    def _clahe(self, x):
        x = x * 255
        x = x.numpy().astype(np.uint8)
        for i in range(x.shape[0]):
            x[i] = self.clahe.apply(x[i])
            # x[i] = cv2.medianBlur(x[i], 3)
        x = torch.from_numpy(x).float()
        x = x / 255
        return x
    
    def _filters(self, x):
        
        self.gauss1 = VT.GaussianBlur(
            kernel_size=(3, 1),
            )
        x = self.gauss1(x)
        xmax = torch.max(x) #torch.quantile(x, 0.95)
        avmax = (xmax + x.median())/2
        xstd = x[x < avmax].std()
        x[x < avmax] = x[x < avmax] * torch.exp(-2*(avmax  - x[x < avmax])**2/xstd**2)
        # x = self.gauss1(x)
        xmax = torch.quantile(x, 0.95)
        avmax = (xmax + x.median())/2
        x = x > avmax
        return x
    
    def _squeeze(self, x):
        x = x.squeeze(0)
        return x
    
    def _interpolate(self, x):
        x = x.unsqueeze(0).unsqueeze(0)
        x = F.interpolate(
            x, 
            size=(self.cfg['nframes'], x.shape[2]), 
            mode='trilinear', 
            align_corners=False
            )
        return x.squeeze(0).squeeze(0)