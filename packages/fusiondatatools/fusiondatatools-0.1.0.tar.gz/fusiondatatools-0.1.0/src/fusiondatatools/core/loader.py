import gzip
import numpy as np
import torch
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
from tqdm.auto import tqdm

from .index import Index


class LoadModule(ABC):
    
    def __init__(self, cfg):
        self.cfg = cfg
        self.setup()
        
    def setup(self):
        self.opener = gzip.open if self.cfg['compress'] else open
        self.cfg['dir'] = Path(self.cfg['dir'])
    
    def filepath(self, idx, attr):
        if self.cfg['compress']:
            return self.cfg['dir'] / f"{attr}_{idx}.npy.gz"
        else:
            return self.cfg['dir'] / f"{attr}_{idx}.npy"
        
    def clear(self):
        if self.cfg['dir'].exists():
            for file in tqdm(self.cfg['dir'].glob('*')):
                file.unlink()
            self.cfg['dir'].rmdir()
            print(f"Directory {self.cfg['dir']} cleared.")
        else:
            print(f"Directory {self.cfg['dir']} does not exist.")
    
    def check(self):
        return self.cfg['dir'].exists() and (len(list(Path('.').glob('*')))) > 0
    
    @abstractmethod
    def save(self, x, idx, attr):
        pass
    
    @abstractmethod
    def finalize(self):
        pass
    
    @abstractmethod
    def initialize(self, *args, **kwds):
        pass
    
    def __call__(self, idx, *args, **kwds):
        pass


class LoadIndividual(LoadModule):
    
    def __init__(self, cfg):
        super().__init__(cfg)
        
    def save(self, x, idx, attr):
        filepath = self.filepath(idx, attr)

        if not self.cfg['overwrite'] and filepath.exists():
             warnings.warn(
                 f"{attr}_{idx} exists in {self.cfg['dir']}. "
                 f"Set overwrite=True to overwrite.", stacklevel=2)
        else:
            x = x.numpy() if isinstance(x, torch.Tensor) else x
            with self.opener(filepath, 'wb') as f: np.save(f, x)
        
    def finalize(self):
        pass
        
    def initialize(self, attr):
        pass
    
    def __call__(self, idx, attr):
        filepath = self.filepath(idx, attr)
        with self.opener(filepath, 'rb') as f: x = np.load(f)
        x = torch.from_numpy(x) if isinstance(x, np.ndarray) else x
        return x


class LoadFull(LoadModule):
    def __init__(self, cfg):
        super().__init__(cfg)
        self.data = {}
        
    def save(self, x, idx, attr):
        if attr not in self.data:
            self.data[attr] = []
        x = x.numpy() if isinstance(x, torch.Tensor) else x
        self.data[attr].append(x)
        
    def finalize(self):
        self.cfg['dir'].mkdir(parents=True, exist_ok=True)
        for attr, data in self.data.items():
            data = np.concatenate(data, axis=0)
            filepath = self.filepath('full', attr)
            with self.opener(filepath, 'wb') as f:
                np.save(f, np.array(data))
        
    def initialize(self, attr):
        filepath = self.filepath('full', attr)
        with self.opener(filepath, 'rb') as f: x = np.load(f)
        x = torch.from_numpy(x) if isinstance(x, np.ndarray) else x
        self.data[attr] = x
        
    def __call__(self, idx, attr):
        return self.data[attr][idx]