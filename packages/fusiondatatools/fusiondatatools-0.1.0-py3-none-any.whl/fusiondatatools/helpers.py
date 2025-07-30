import numpy as np
import torch
from pathlib import Path

minmax = lambda x: (x - x.min()) / (x.max() - x.min())

def get_shots(directory, stage):
    directory = Path(directory)
    shot_directory = directory / stage
    shots = [int(s.stem) for s in shot_directory.glob('*.parquet')]
    shots.sort()
    return shots

def get_ece_channels(nums='all'):
    if nums == 'all': channels = [f'ece{i:02d}' for i in range(1,41)]
    elif isinstance(nums, list): channels = [f'ece{i:02d}' for i in nums]
    else: raise ValueError("Invalid input for nums. Must be 'all' or a list of integers.")
    return channels

def sigmoid(x, a=1, b=0):
    return 1 / (1 + np.exp(-a * (x - b)))

def gauss(x,a,mu,sigma):
    return a*np.exp(-(x-mu)**2/(2*sigma**2))

def sigma_threshold(x, k=3, dim=0):
    med = torch.median(x, dim=dim)
    sig = torch.std(x, dim=dim)
    
    print(med.shape, sig.shape, k)
    return med + k * sig