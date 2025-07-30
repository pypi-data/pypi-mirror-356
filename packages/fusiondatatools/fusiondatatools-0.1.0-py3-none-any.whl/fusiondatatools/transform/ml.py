import torch

from specseg.transform import SignalMLTransform

class AEEPTransform0(SignalMLTransform):
    
    def __init__(self, cfg):
        super().__init__(cfg)
        self.window = torch.hann_window(
            self.cfg['nfft'], periodic=True)
        
    def config(self, sample):
        features = sample
        self.cfg['nframes'] = features.shape[1]
        
    def transform_feature(self, x):
        x = self._ensure_dimensions(x)
        x = self._stft(x)
        x = self._normalize(x)
        return x
    
    def transform_label(self, x):
        x = self._interpolate(x)
        return x
    
    def _stft(self, x):
        x = torch.stft(
            x,
            n_fft=self.cfg['nfft'],
            hop_length = self.cfg['nfft']//2,
            window=self.window,
            center=True,
            pad_mode='reflect',
            normalized=False,
            onesided=True,
            return_complex=True
            )
        return torch.log(torch.abs(x))
    
    def _ensure_dimensions(self, x):
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
        if len(x.shape) == 2:
            pass
        return x
    
    def _normalize(self, x):
        # x = x[:,30:-60]
        x = x[:,6:]
        vmin = torch.quantile(x, 0.05)
        vmax = torch.quantile(x, 0.95)
        x = torch.clamp(x, vmin, vmax)
        return x
    
    def _interpolate(self, x):
        x = x.unsqueeze(0).unsqueeze(0)
        x = F.interpolate(
            x, 
            size=(self.cfg['nframes'], x.shape[2]), 
            mode='bilinear', 
            align_corners=False
            )
        return x.squeeze(0)