import os
import warnings

import numpy as np
from pathlib import Path
from typing import Union

import pandas as pd


class ParquetFileReader:
    """
    Parquet file, reads the file and can access trough properties

    """

    def __init__(self, filepath: str, qa=True, verbose=False, unit=''):
        self.filepath = filepath

        self._df = pd.read_parquet(filepath)
        self._df.index = pd.to_datetime(self._df.index) # Convert to datetimeindex
        self._df.sort_index(inplace=True) # Sort the index
        self._update_properties()

        self.unit = unit
        self.verbose = verbose

        if self.verbose:
            print(f"Loaded {len(self.channels)} channels: {','.join(self.channels)}")

        if qa:
            self.missing_samples
            self.nan_samples

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, new_df):
        self._df = new_df
        self._df.index = pd.to_datetime(new_df.index)
        self._update_properties() # Also update all related properties

    def _update_properties(self):
        """
        Compute properties for ease of use whenever a dataframe is updated

        :return:
        """
        self.channels = list(self.df.columns)
        self.start_timestamp = self.df.index[0]
        self.fs = 1 / (self.df.index[1] - self.df.index[0]).total_seconds()  # Sampling frequency in Hz
        self.duration = len(self.df) / self.fs
        self.time = (self.df.index - self.start_timestamp).total_seconds()

    def to_sep005(self):
        """_summary_

        Args:

        Returns:
            list: signals
        """
        signals = []
        for chan in self.channels:
            data = self.df[chan].to_numpy()
            fs_signal = len(data) / self.duration

            signal = {
                'name': chan,
                'data': data,
                'start_timestamp': str(self.start_timestamp),
                'fs': fs_signal,
                'unit_str': self.unit
            }
            signals.append(signal)

        return signals

    @property
    def missing_samples(self):
        """
        Check if the sampling frequency is maintained properly
        :return:
        """
        # check the index matches the sampling frequency
        differences_2nd_order = np.diff(self.time, n=2)  # Calculate the 2nd order differences to find gaps
        is_equidistant = np.all(np.isclose(differences_2nd_order, 0))  # Check if all differences are the same, up to precision
        if not is_equidistant:
            differences = np.diff(self.time) # Slower but required to estimate the number of missing samples
            no_missing_samples = round(sum(differences*self.fs-1))
            raise ValueError(f'{no_missing_samples} Sample(s) missing from all channels')
        if self.verbose and is_equidistant:
            print('QA (missing samples) : Imported signals are equidistant spaced on index')

    @property
    def nan_samples(self):
        """
        Check if there are samples as NaN
        :return:
        """
        nan_counts = self.df.isnull().sum()
        nan_counts = nan_counts[nan_counts > 0]

        if not nan_counts.empty:
            summary = ', '.join(f'{col}: {count}' for col, count in nan_counts.items())
            raise ValueError(f'Channels contain NaN samples. NaN counts: ({summary})')
        if self.verbose:
            print('QA (NaN samples) : Imported signals contain no NaNs')

    def resolve_missing_samples(self, inplace=True, **kwargs):
        """
        Interpolate missing samples using a linear interpolation

        Additional kwargs are passed on directly in pd.DataFrame.interpolate

        :return:
        """

        end_timestamp = self.df.index[-1]
        dt = int(1/self.fs*1e6) # micro seconds

        continuous_index = pd.date_range(start=self.start_timestamp, end=end_timestamp, freq=f'{dt}us')
        df_rs = self.df.reindex(continuous_index)

        # Now, perform linear interpolation
        df_interpolated = df_rs.interpolate(method='linear', **kwargs)

        if inplace:
            self.df = df_interpolated
        else:
            return df_interpolated



def read_parquet(path: Union[str, Path], **kwargs) -> list:
    """
    Primary function to read fbgs files based on path


    """
    if not os.path.isfile(path):
        warnings.warn('FAILED IMPORT: No parquet file at: ' + path, UserWarning)
        signals = []
        return signals

    meas_file = ParquetFileReader(path, **kwargs)

    return meas_file.to_sep005()