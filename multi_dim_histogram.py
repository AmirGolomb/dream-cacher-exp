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

# def avg_value_2d(x, y, values, bins: int | Sequence[int] = 10, range = None):
#     # noinspection GrazieInspection
#     """
#         Create a 2D histogram where each bin contains the average of `values` for points in that bin.
#
#         Parameters:
#             x:  array_like: shape (N,).
#                 An array containing the x coordinates of the points.
#             y:  array_like: shape (N,).
#                 An array containing the y coordinates of the points.
#             values : array_like: Values to average in each bin.
#             bins (int or [int, int]): Number of bins along each dimension (x, y).
#             range ([(float, float), (float, float)], optional): The range of the histogram along each dimension.
#
#         Returns:
#             avg_hist (2D array): 2D array of average values in each bin.
#             xedges (1D array): Bin edges along the x-axis.
#             yedges (1D array): Bin edges along the y-axis.
#         """
#     # Ensure input arrays have matching lengths
#     if len(x) != len(y) or len(x) != len(values):
#         raise ValueError("x, y, and values must have the same length")
#
#     # Create a 2D histogram for sums of values
#     hist_sum, xedges, yedges = np.histogram2d(x, y, bins=bins, range=range, weights=values)
#
#     # Create a 2D histogram for counts of points
#     hist_count, _, _ = np.histogram2d(x, y, bins=bins, range=range)
#
#     # Avoid division by zero: set bins with no points to NaN
#     with np.errstate(divide='ignore', invalid='ignore'):
#         avg_hist = np.divide(hist_sum, hist_count)
#         avg_hist[hist_count == 0] = np.nan  # Handle empty bins
#
#     return avg_hist, xedges, yedges



