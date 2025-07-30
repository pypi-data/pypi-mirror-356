import copy
import pandas as pd
from pathlib import Path

import torch
from torch.utils.data import Dataset

from typing import Optional
from typing import Union, Type

from .transform import SignalTransformer
from .index import Index


class SignalDataset(Dataset):
    def __init__(
        self, stage: str, shots: list[int],
        inputs: list[str], labels: list[str],
        cfg: dict, indexer: Index,
        transform: Optional[SignalTransformer],
        ):

        self.stage = stage
        self.inputs = inputs
        self.labels = labels
        self.shots = shots
        self.transform = transform
        self.cfg = copy.deepcopy(cfg)

        self.data_dir = None
        self._setup_status = False
        self.on_off = True
        
        self.indexer: Index = indexer
        
        self._setup()
    
    def _setup(self):
        
        if self._setup_status:
            print("Dataset already setup. Skipping.")
            return
        
        self.indexer = Index(self.cfg)  # default
        
        self._configure_subclass()
        self._configure_stage()
        if self.cfg.get('fs_khz') and self.cfg.get('duration_ms') \
            and self.cfg.get('window_ms') and self.cfg.get('hop_ms'):
            self._configure_timebasis()
        if self.shots is not None: self._configure_index()
        if self.transform is not None: self._configure_transform() 
        
        self._setup_status = True
        print(f"Dataset setup complete")
    
    def _configure_subclass(self):
        pass
        
    def _configure_stage(self):
        print(f"Stage: {self.stage.capitalize()}", flush=True)
        assert self.stage in ['train', 'valid', 'test']
        self.data_dir = Path(self.cfg['root_dir']) / self.stage
        
    def _configure_timebasis(self, fs_khz=None, duration_ms=None, window_ms=None, hop_ms=None):
        
        self.indexer.time_index(
            fs_khz=fs_khz, duration_ms=duration_ms,
            window_ms=window_ms, hop_ms=hop_ms)
        self.indexer.cfg['input_count'] = len(self.inputs)
        
        print(f"Number windows per shot: {self.indexer.cfg['window_count']}", flush=True)
        print(f"Number of inputs per shot: {self.indexer.cfg['input_count']}", flush=True)
        
    def _configure_index(self, shots=None):
        
        if shots is not None: self.shots = shots
        
        self.indexer.cfg['shot_count'] = len(self.shots)
        self.indexer.total_samples()
        
        print(f"Number of shots: {self.indexer.cfg['shot_count']}", flush=True)
        print(f"Total length of dataset: {self.indexer.cfg['sample_count']}", flush=True)
        
    def _configure_transform(self):
        
        if self.transform is None:
            print("No transform provided. Skipping transform configuration.")
            return
        
        load_enabled = self.cfg['load']['load_enabled']
        self.cfg['load']['load_enabled'] = False
        sample = self[0]
        self.transform.configure(sample)
        self.cfg['load']['load_enabled'] = load_enabled
        print(f"Transform successfully applied to the dataset.")
        
    def location(self, idx):
        
        sample_idx, inputs_idx, window_idx = self.indexer.location(idx)
        shot = self.shots[sample_idx]
        inputs = [self.inputs[input_idx] for input_idx in inputs_idx]
        window = window_idx
        return shot, inputs, window
    
    def _frameidx(self, window=None):

        return self.indexer.frameidx(window)
        
    def __len__(self):
        
        if self.cfg['sample_count'] is None: raise ValueError(
            "Dataset length is not defined. Please call index() method first.")
        return self.indexer.cfg['sample_count']
    
    def __call__(self, shot, columns=None, window=0):
        if columns is None: columns = self.inputs
        if window >= self.indexer.cfg['window_count']: raise ValueError(
            f"window {window} is out of range of {self.indexer.cfg['window_count']}")
        
        start_idx, end_idx = self.indexer.frameidx(window)
        path = self.data_dir / f'{shot}.parquet' # type: ignore
        
        x = pd.read_parquet(path=path, columns=columns)
        x = x.to_numpy()[start_idx:end_idx].T
        x = torch.from_numpy(x)
        return x
    
    def __getitem__(self, idx):
        output = {}
        location = self.location(idx)
        
        feature = self(*location)
        if self.transform:
            feature = self.transform(feature, 'feature')
        output['feature'] = feature.share_memory_()
        
        if self.cfg['return_label']:
            output['label'] = self(location[0], self.labels, location[2])
            if self.transform:
                output['label'] = self.transform(output['label'], 'label')
            output['label'] = output['label'].share_memory_()
        
        if self.cfg['return_state']:
            on_off_labels = [x + '_state' for x in location[1]]
            output['state'] = self(location[0], on_off_labels, location[2])
            if self.transform:
                output['state'] = self.transform(output['state'], 'state')
            output['state'] = output['state'].share_memory_()
            
        return output