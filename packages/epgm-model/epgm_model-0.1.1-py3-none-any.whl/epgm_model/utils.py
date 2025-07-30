'''
Utility functions for the EPGM model implementation.

Author: Haris Masood
Date: 2025-05-26
Version: 1.0
'''

import numpy as np
import pandas as pd

def AGO(data):
    """
    Perform the Accumulated Generating Operation (AGO) on the input data.

    Parameters:
    data (pd.Series or np.ndarray): Input data to be transformed.

    Returns:
    pd.Series or np.ndarray: Transformed data after applying AGO.
    """

    if isinstance(data, pd.Series):
        return data.cumsum()
    elif isinstance(data, np.ndarray):
        return np.cumsum(data)
    else:
        raise TypeError("Input data must be a pandas Series or a numpy ndarray.")
    
def IAGO(data):
    """
    Perform the Inverse Accumulated Generating Operation (IAGO) on the input data.

    Parameters:
    data (pd.Series or np.ndarray): Input data to be transformed.

    Returns:
    pd.Series or np.ndarray: Transformed data after applying IAGO.
    """

    if isinstance(data, pd.Series):
        return data.diff().loc[1:] # Skip the first NaN value
    elif isinstance(data, np.ndarray):
        return np.diff(data)
    else:
        raise TypeError("Input data must be a pandas Series or a numpy ndarray.")
    

def Z_one(data, r1):
    """
    Perform the Z_one transformation on the input data.

    Parameters:
    data (pd.Series or np.ndarray): Input data to be transformed.

    Returns:
    pd.Series or np.ndarray: Transformed data after applying Z_one.
    """

    if isinstance(data, pd.Series):
        return ((r1 * data.iloc[1:]).values + ((1-r1)*data.iloc[:-1]))
    elif isinstance(data, np.ndarray):
        return (r1 * data[1:]) + ((1-r1)*data[:-1])
    else:
        raise TypeError("Input data must be a pandas Series or a numpy ndarray.")

