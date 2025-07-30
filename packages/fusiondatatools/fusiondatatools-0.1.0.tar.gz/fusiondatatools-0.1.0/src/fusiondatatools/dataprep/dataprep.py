import numpy as np
import polars as pl
import pickle as pkl
import h5py
from pathlib import Path
from scipy.signal import resample
from scipy.interpolate import interp1d

from specseg import parmap

def resample_nearest(y, new_len):
    return interp1d(np.linspace(0, 1, len(y)), y, kind='cubic')(np.linspace(0, 1, new_len))


def extract(
    shot: int,
    directory: Path,
    ) -> pl.DataFrame:
    
    path = (directory / f'{shot}' / 'co2').with_suffix('.h5')
    
    with h5py.File(path, 'r') as hf:
        co2_time = hf['co2_time'][:]
        dp1r0uf = hf['dp1r0uf'][:]
        dp1v1uf = hf['dp1v1uf'][:]
        dp1v2uf = hf['dp1v2uf'][:]
        dp1v3uf = hf['dp1v3uf'][:]
        
    df = pl.DataFrame({
        'time': co2_time,
        'r0': dp1r0uf,
        'v1': dp1v1uf,
        'v2': dp1v2uf,
        'v3': dp1v3uf
    })
    
    return df


def transform(
    df: pl.DataFrame,
    num_samples: int,
    start_time: float,
    end_time: float,
    labels: np.ndarray=None,
    ) -> pl.DataFrame:
    
    # Filter the dataframe based on time
    if df['time'].min() > start_time: print(f"Start time {start_time} is greater than the minimum time in the dataframe.")
    if df['time'].max() < end_time: print(f"End time {end_time} is less than the maximum time in the dataframe.")
    df = df.filter((df['time'] >= start_time) & (df['time'] <= end_time))
    
    # Resample the data to the desired number of samples
    new_time = np.linspace(start_time, end_time, num_samples)
    
    df_temp = pl.DataFrame({
        'time': new_time,
        'r0': np.zeros(num_samples),
        'v1': np.zeros(num_samples),
        'v2': np.zeros(num_samples),
        'v3': np.zeros(num_samples)
    })
    
    for col in ['r0', 'v1', 'v2', 'v3']:
        resampled_data = resample(df[col].to_numpy(), num_samples)
        df_temp = df_temp.with_columns(
            pl.Series(col, resampled_data)
        )
    
    df = df_temp
    
    # Convert float in ms to timedelta
    df = df.with_columns(
        (pl.col("time") * 1_000_000).cast(pl.Duration("ns")).alias("duration")
        )
    
    # switch duration with time and remove time
    df = df.with_columns(
        pl.col("duration").alias("time")
    ).drop("duration")
    
    # include labels
    if labels:
        for idx, col in enumerate(['lfm', 'bae', 'eae', 'rsae', 'tae']):
            label = labels[:, idx]
            label = resample_nearest(label, num_samples).astype(bool)
            df = df.with_columns(
                pl.Series(col, label)
            )
    
    return df


def load(
    df: pl.DataFrame,
    directory: Path,
    shot: int
    ) -> None:
    
    # Save the dataframe to a parquet file
    output_path = directory / f'{shot}.parquet'
    df.write_parquet(output_path, compression='lz4')

def process_feature(data, cfg): # no labels
    shot = data
    df = extract(shot, cfg['raw_dataset_directory'])
    df = transform(df, cfg['num_samples'], cfg['start_time'], cfg['end_time'])
    df = load(df, cfg['output_directory_train'], shot)
    return df

def process_train(data, cfg):
    shot, label = data
    df = extract(shot, cfg['raw_dataset_directory'])
    df = transform(df, cfg['num_samples'], cfg['start_time'], cfg['end_time'], label)
    df = load(df, cfg['output_directory_train'], shot)
    return df

def process_val(data, cfg):
    shot, label = data
    df = extract(shot, cfg['raw_dataset_directory'])
    df = transform(df, cfg['num_samples'], cfg['start_time'], cfg['end_time'], label)
    df = load(df, cfg['output_directory_valid'], shot)
    return df
    

def main():
    
    fs_target = 500 # kHz
    start_time = 0 # ms
    end_time = 2000 # ms
    num_samples = int((end_time - start_time) * fs_target)

    benchmark_dataset = '/scratch/gpfs/nc1514/specseg/data/co2_250_detector.pkl'
    raw_dataset_directory = '/projects/EKOLEMEN/aza_lenny_data1/h5data'
    output_directory = '/scratch/gpfs/nc1514/specseg/data/interferometer'
    
    benchmark_dataset = Path(benchmark_dataset)
    raw_dataset_directory = Path(raw_dataset_directory)
    output_directory = Path(output_directory)
    
    output_directory_train = output_directory / 'train'
    output_directory_valid = output_directory / 'valid'
    output_directory_train.mkdir(parents=True, exist_ok=True)
    output_directory_valid.mkdir(parents=True, exist_ok=True)
    
    all_shots = [file.stem for file in raw_dataset_directory.iterdir()]
    # all_shots = [178631]
    cfg = {
        'num_samples': num_samples,
        'start_time': start_time,
        'end_time': end_time,
        'raw_dataset_directory': raw_dataset_directory,
        'output_directory_train': output_directory_train,
        'output_directory_valid': output_directory_valid,
    }

    # [train_shots, X_train,y_train,valid_shots, X_valid,y_valid] = pkl.load(open(benchmark_dataset,'rb'))
    
    # process_train((train_shots[0], y_train[0]), cfg)
    
    # train_data = list(zip(train_shots, y_train))
    # valid_data = list(zip(valid_shots, y_valid))
    print(f"Processing data...")
    mapper = parmap.ParallelMapper()
    mapper(process_feature, all_shots, cfg=cfg)
    print(f"Finished processing!")
    # mapper(process_train, train_data, cfg=cfg)
    # mapper(process_val, valid_data, cfg=cfg)
    
if __name__ == '__main__':
    main()