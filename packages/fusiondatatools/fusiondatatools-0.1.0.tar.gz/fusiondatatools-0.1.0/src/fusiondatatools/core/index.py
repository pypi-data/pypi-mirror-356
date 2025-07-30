from typing import Any


class Index:
    REQUIRED_KEYS = {
        'fs_khz': (float, lambda x: x > 0),
        'duration_ms': (float, lambda x: x >= 0),
        'window_ms': (float, lambda x: x > 0),
        'hop_ms': (float, lambda x: x > 0),
    }
        
    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        self._validate_config()
        
    def _validate_config(self):
        missing = [k for k in self.REQUIRED_KEYS if k not in self.cfg]
        if missing: raise KeyError(f"Missing required cfg keys: {missing!r}")

        for key, (typ, test) in self.REQUIRED_KEYS.items():
            val = self.cfg[key]
            if not isinstance(val, typ): raise TypeError(f"cfg['{key}'] must be {typ.__name__}, got {type(val).__name__}")
            if not test(val): raise ValueError(f"cfg['{key}'] failed validation, got {val!r}")
    
    def time_index(self, fs_khz=None, duration_ms=None, window_ms=None, hop_ms=None):
        for name, override in (
            ('fs_khz', fs_khz),
            ('duration_ms', duration_ms),
            ('window_ms', window_ms),
            ('hop_ms', hop_ms)):
            if override is not None: self.cfg[name] = override
        self._validate_config()
        
        start_ms = self.cfg.get('start_ms', 0)
        self.cfg['start_idx']    = int(start_ms                 *   self.cfg['fs_khz'])
        self.cfg['duration_idx'] = int(self.cfg['duration_ms']  *   self.cfg['fs_khz'])
        self.cfg['window_idx']   = int(self.cfg['window_ms']    *   self.cfg['fs_khz'])
        self.cfg['hop_idx']      = int(self.cfg['hop_ms']       *   self.cfg['fs_khz'])
        self.cfg['window_count'] = ((self.cfg['duration_idx']   -   self.cfg['window_idx'])
                                    //  self.cfg['hop_idx']) + 1
    
    def frameidx(self, window):
        start_idx = self.cfg['start_idx'] + window * self.cfg['hop_idx']
        end_idx = start_idx + self.cfg['window_idx']
        return start_idx, end_idx
    
    def total_samples(self):
        raise NotImplementedError("Subclasses must implement total_samples method")
    
    def location(self, idx):
        raise NotImplementedError("Subclasses must implement location method")


class IndividualIndex(Index):
        
    def total_samples(self):
        self.cfg['sample_count'] = self.cfg['shot_count'] * self.cfg['window_count'] * self.cfg['input_count']
    
    def location(self, idx):
        sample_idx = idx // (self.cfg['window_count'] * self.cfg['input_count'])
        input_idx = (idx // self.cfg['window_count']) % self.cfg['input_count']
        window_idx = idx % self.cfg['window_count']
        return sample_idx, [input_idx], window_idx


class BatchIndex(Index):
        
    def total_samples(self):
        self.cfg['sample_count'] = self.cfg['shot_count'] * self.cfg['window_count']
    
    def location(self, idx):
        sample_idx = idx // self.cfg['window_count']
        input_idx = list(range(self.cfg['input_count']))
        window_idx = idx % self.cfg['window_count']
        return sample_idx, input_idx, window_idx