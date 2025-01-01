from typing import Sequence
import numpy as np
import matplotlib.pyplot as plt


def multi_dim_histogram(sample, values, bins: int | Sequence[int]):
    # Ensure input arrays have matching lengths
    n_vals = len(values)
    for dim in sample:
        if not len(dim) == n_vals:
            raise ValueError("x, y, and values must have the same length")

    # Create a histogram for sums of values
    hist_sum, histogram_edges = np.histogramdd(sample.T, bins=bins, range=None, weights=values)

    # Create a histogram for counts of points
    hist_count, _ = np.histogramdd(sample.T, bins=bins, range=None)

    # Avoid division by zero: set bins with no points to NaN
    with np.errstate(divide='ignore', invalid='ignore'):
        avg_hist = np.divide(hist_sum, hist_count)
        avg_hist[hist_count == 0] = np.nan  # Handle empty bins

    print(f'avg_hist={np.unique(avg_hist)}')

    return avg_hist, histogram_edges




