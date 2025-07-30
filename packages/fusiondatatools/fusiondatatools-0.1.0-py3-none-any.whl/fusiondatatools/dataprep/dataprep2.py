import re
import numpy as np
import polars as pl
import h5py
from pathlib import Path
from scipy.interpolate import interp1d
from datetime import time, timedelta
from . import parmap

# -------------------------------------------------------------------
# Core utilities
# -------------------------------------------------------------------

def resample_nearest(y: np.ndarray, new_len: int) -> np.ndarray:
    return interp1d(np.linspace(0, 1, len(y)), y, kind='cubic')(np.linspace(0, 1, new_len))


def infer_interval(times: np.ndarray) -> str:
    """Infer a sampling interval string from a numeric time array (assumed uniform)."""
    dt = (times[1] - times[0])
    # assume times in ms, want output as "<dt>ms"
    return f"{float(dt)}ms"

# -------------------------------------------------------------------
# Extraction
# -------------------------------------------------------------------

def extract_h5(
    shot: int,
    directory: Path,
    sensor: str,
    field_map: dict[str, str] | None = None
) -> pl.DataFrame:
    """
    Generic extractor: opens {directory}/{shot}/{sensor}.h5,
    reads each dataset into a column, optionally renaming with exact or regex.
    """
    path = (directory / f"{shot}" / sensor).with_suffix(".h5")
    data = {}
    with h5py.File(path, "r") as hf:
        for key in hf.keys():
            new_name = key
            if field_map:
                # exact key first
                if key in field_map:
                    new_name = field_map[key]
                else:
                    # regex patterns
                    for pat, repl in field_map.items():
                        if re.fullmatch(pat, key):
                            # use re.sub so groups work
                            new_name = re.sub(pat, repl, key)
                            break
            data[new_name] = hf[key][:]
    df = pl.DataFrame(data)
    return df

# -------------------------------------------------------------------
# Transformation
# -------------------------------------------------------------------

def transform(
    df: pl.DataFrame,
    time_col: str,
    fs: int,
    start_time: float,
    end_time: float,
    label_cols: list[str] | None = None,
    labels: np.ndarray | None = None,
) -> pl.DataFrame:
    
    df = df.filter(
        (pl.col(time_col) >= start_time) & (pl.col(time_col) <= end_time)
    )

    df = df.with_columns(
        (pl.col("time") * 1000_000).cast(pl.Duration("ns")).alias("time")
    )
    
    
    interval = 1 / fs
    interval = timedelta(milliseconds=interval)
    start = time(0, 0, int(start_time//1000), int(start_time%1000*1000))
    end = time(0, 0, int(end_time//1000), int(end_time%1000*1000))
    
    grid= pl.time_range(
        start=start,
        end=end,
        interval=interval,
        eager=True,
    ).to_frame(
        name="time",
    ).with_columns(
        pl.col("time").cast(pl.Duration("ns")).alias("time"),
    )
    
    df = grid.join(
        df,
        on="time",
        how="full",
        coalesce=True,
    ).sort('time').interpolate()
    
    df = grid.join(
        df,
        on="time",
        how="left",
    )
    
    num_samples = int((end_time - start_time) * fs)
    # 6) add label columns if provided
    if label_cols and labels is not None:
        for idx, lc in enumerate(label_cols):
            lab = resample_nearest(labels[:, idx], num_samples).astype(bool)
            df = df.with_columns(pl.Series(lc, lab))

    return df

# -------------------------------------------------------------------
# Loader
# -------------------------------------------------------------------

def load_parquet(
    df: pl.DataFrame,
    directory: Path,
    shot: int
) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    df.write_parquet(directory / f"{shot}.parquet", compression="lz4")

# -------------------------------------------------------------------
# High-level pipeline
# -------------------------------------------------------------------
def process_shot(
    shot: int,
    cfg: dict,
    labels: np.ndarray | None = None
) -> None:
    """
    Drives extract→transform→load for one shot.
    """
    dfs = []
    for i, sensor in enumerate(cfg["sensors"]):
        fm = cfg.get("field_maps", {}).get(sensor)
        try:
            dfs.append(extract_h5(shot, cfg["raw_dataset_directory"], sensor, fm))
        except FileNotFoundError:
            print(f"File not found for shot {shot} and sensor {sensor}.")
            return
    df = pl.concat(dfs, how="diagonal_relaxed")
    df = transform(df, cfg["time_col"], cfg["fs"], cfg["start_time"], cfg["end_time"], cfg.get("label_cols"), labels)

    # select output dir
    out_dir = cfg["output_directory_valid"] if labels is not None else cfg["output_directory_train"]
    load_parquet(df, out_dir, shot)

# -------------------------------------------------------------------
# Main entry
# -------------------------------------------------------------------
def main():
    cfg = {
        "sensors": ["co2", "ece"],
        "field_maps": {
            "co2": {
                "co2_time": "time",
                r"dp1r0uf": "r0",
                r"dp1v([1-3])uf": r"v\1",
            },
            # Change: capture number after tecef and keep it
            "ece": {r"\\tecef(\d+)": r"ece\1"},
        },
        "time_col": "time",
        "fs": 500,
        "start_time": 0.0,
        "end_time": 2000.0,
        "raw_dataset_directory": Path("/projects/EKOLEMEN/aza_lenny_data1/h5data"),
        "output_directory_train": Path("/scratch/gpfs/nc1514/specseg/data/co2ece/train"),
        "output_directory_valid": Path("/scratch/gpfs/nc1514/specseg/data/co2ece/valid"),
        "label_cols": ["lfm", "bae", "eae", "rsae", "tae"],
    }
    cfg["num_samples"] = int(
        (cfg["end_time"] - cfg["start_time"]) * cfg["fs"]
        )
    

    all_shots = [int(p.stem) for p in cfg["raw_dataset_directory"].iterdir()]
    mapper = parmap.ParallelMapper()
    mapper(process_shot, all_shots, cfg=cfg)
    # for shot in all_shots: process_shot(shot, cfg)

if __name__ == "__main__":
    main()
