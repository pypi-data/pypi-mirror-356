import re
import numpy as np
import pandas as pd
import polars as pl
import h5py
from pathlib import Path
from scipy.interpolate import interp1d
from scipy.signal import resample, resample_poly
from sklearn.model_selection import train_test_split
from datetime import time, timedelta
from specseg.core import parmap
import logging

log = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Core utilities
# -------------------------------------------------------------------

def resample_nearest(y: np.ndarray, new_len: int) -> np.ndarray:
    orig_len = len(y)
    gcd = np.gcd(orig_len, new_len)
    up = new_len // gcd
    down = orig_len // gcd
    return resample_poly(y, up, down)
    # return resample(y, new_len)
    # return interp1d(np.linspace(0, 1, len(y)), y, kind='cubic')(np.linspace(0, 1, new_len))


def infer_interval(times: np.ndarray) -> str:
    """Infer a sampling interval string from a numeric time array (assumed uniform)."""
    dt = (times[1] - times[0])
    # assume times in ms, want output as "<dt>ms"
    return f"{float(dt)}ms"

# -------------------------------------------------------------------
# Extraction
# -------------------------------------------------------------------

def extract(
    shot: int,
    directory: Path,
    sensor: str,
) -> pd.DataFrame:
    """
    Generic extractor: opens {directory}/{shot}/{sensor}.h5,
    reads each dataset into a column, optionally renaming with exact or regex.
    """
    path = (directory / str(shot)).with_suffix(".h5")
    df = pd.read_hdf(path, key=sensor)
    return df

# -------------------------------------------------------------------
# Transformation
# -------------------------------------------------------------------

def transform(
    df: pd.DataFrame,
    start_time: float,
    end_time: float,
    fs: float,
    
) -> pd.DataFrame:
    
    # get sampling frequency
    fs_raw = len(df) / (df.index[-1] - df.index[0])
    
    # crop time
    df = df.loc[(df.index >= start_time) & (df.index <= end_time)]
    
    # resample
    num = len(df)
    num = int(num * fs / fs_raw)
    
    df = pd.DataFrame(
        {col: resample(df[col].values, num) for col in df.columns},
        index=np.linspace(df.index[0], df.index[-1], num)
    )
    
    # mark on-off states
    start_nan = (df.index[0] - start_time) * fs
    end_nan = (end_time - df.index[-1]) * fs
    start_pad = pd.DataFrame(
        0, index=pd.RangeIndex(start=int(start_nan)), columns=df.columns)
    end_pad = pd.DataFrame(
        0, index=pd.RangeIndex(start=int(len(df) + start_nan), stop=int(len(df) + start_nan + end_nan)), columns=df.columns)
    
    df_state = pd.DataFrame(True, index=df.index, columns=df.columns)
    start_pad_state = pd.DataFrame(False, index=start_pad.index, columns=df.columns)
    end_pad_state = pd.DataFrame(False, index=end_pad.index, columns=df.columns)
    
    df = pd.concat([start_pad, df, end_pad], ignore_index=True)
    df_state = pd.concat([start_pad_state, df_state, end_pad_state], ignore_index=True)
    df_state.columns = [f"{col}_state" for col in df.columns]
    
    # combine data with state
    df = df.astype(np.float32)
    df_state = df_state.astype(np.bool)
    df = pd.concat([df, df_state], axis=1)
    
    # convert time to ms
    df = df.rename_axis("time")
    df.index = pd.to_timedelta(df.index, unit='ms')

    return df

# -------------------------------------------------------------------
# Loader
# -------------------------------------------------------------------

def load_parquet(
    df: pd.DataFrame,
    directory: Path,
    shot: int
) -> None:
    df.to_parquet(directory / f"{shot}.parquet", compression="lz4")

# -------------------------------------------------------------------
# High-level pipeline
# -------------------------------------------------------------------
def process_shot(
    shot: int,
    cfg: dict,
    out_dir: Path | None = None,
) -> None:
    """
    Drives extract→transform→load for one shot.
    """
    try:
        dfs = []
        for i, sensor in enumerate(cfg["sensors"]):
            fm = cfg.get("field_maps", {}).get(sensor)
            try:
                df = extract(shot, cfg["raw_dataset_directory"], sensor)
            except FileNotFoundError:
                print(f"File not found for shot {shot} and sensor {sensor}.")
                return
            try:
                if sensor == "ece_cali":
                    df.columns = [f"ece{col}" if col != "time" else col for col in df.columns]
                df = transform(df, cfg["start_time"], cfg["end_time"], cfg["fs"])
            except ValueError:
                print(f"Error transforming data for shot {shot} and sensor {sensor}.")
                return
            dfs.append(df)
            
        df = pd.concat(dfs, axis=1)

        load_parquet(df, out_dir, shot)
    except Exception as e:
        log.error(f"Error processing shot {shot}: {e}")

# -------------------------------------------------------------------
# Main entry
# -------------------------------------------------------------------
def main():
    cfg = {
        "sensors": ["magnetics_high_resolution", "co2_phase", "ece_cali"],
        "time_col": "time",
        "fs": 500,
        "start_time": 200.0,
        "end_time": 3200.0,
        "raw_dataset_directory": Path("/scratch/gpfs/EKOLEMEN/d3d_fusion_data/"),
        "output_directory_train": Path("/scratch/gpfs/nc1514/specseg/data/foundation_high_frequency/train"),
        "output_directory_valid": Path("/scratch/gpfs/nc1514/specseg/data/foundation_high_frequency/valid"),
        "label_cols": ["lfm", "bae", "eae", "rsae", "tae"],
    }
    cfg["num_samples"] = int(
        (cfg["end_time"] - cfg["start_time"]) * cfg["fs"]
        )
    

    all_shots = [int(p.stem) for p in cfg["raw_dataset_directory"].iterdir()]
    all_shots.sort()
    all_shots = all_shots[::10]
    train_shots, valid_shots = train_test_split(all_shots, test_size=0.2, random_state=42)
    print(f"Preparing {len(train_shots)} training and {len(valid_shots)} validation shots.")
    
    train_path = Path(cfg["output_directory_train"])
    valid_path = Path(cfg["output_directory_valid"])
    train_path.mkdir(parents=True, exist_ok=True)
    valid_path.mkdir(parents=True, exist_ok=True)
    
    process_shot(178631, cfg, out_dir=train_path) # for testing
    # mapper = parmap.ParallelMapper()
    # mapper(process_shot, train_shots, cfg=cfg, out_dir=train_path)
    # mapper(process_shot, valid_shots, cfg=cfg, out_dir=valid_path)
    # for shot in all_shots: process_shot(shot, cfg) # serial

if __name__ == "__main__":
    main()
