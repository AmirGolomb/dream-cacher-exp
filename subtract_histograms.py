from typing import Sequence
import numpy as np

def subtract_histograms(sample1, values1, sample2, values2, bins: int | Sequence[int]):
    """
    Compute the difference between two 3D histograms where bins represent average values in 3D space.
    Only include bins where both histograms have valid values.

    Parameters:
        sample1 (list of ndarray): List of x, y, z coordinates for the first set of points.
        values1 (ndarray): Values associated with points in the first set.
        sample2 (list of ndarray): List of x, y, z coordinates for the second set of points.
        values2 (ndarray): Values associated with points in the second set.
        bins (int or Sequence[int]): Number of bins for the histogram in each dimension.

    Returns:
        diff_hist (ndarray): Difference between histograms.
        edges (list of ndarray): Bin edges.
    """

    # Define a common grid for rebinning based on the range of all points
    ranges = [(min(np.min(sample1[i]), np.min(sample2[i])),
               max(np.max(sample1[i]), np.max(sample2[i]))) for i in range(3)]

    # Create a single set of bin edges for all datasets
    common_edges = [np.linspace(r[0], r[1], bins[i] + 1) if isinstance(bins, Sequence) else
                    np.linspace(r[0], r[1], bins + 1) for i, r in enumerate(ranges)]

    # Rebin both datasets
    hist_sum1, _ = np.histogramdd(sample1, bins=common_edges, weights=values1)
    hist_count1, _ = np.histogramdd(sample1, bins=common_edges)

    hist_sum2, _ = np.histogramdd(sample2, bins=common_edges, weights=values2)
    hist_count2, _ = np.histogramdd(sample2, bins=common_edges)

    # Calculate average histograms with the common grid
    with np.errstate(divide='ignore', invalid='ignore'):
        avg_hist1 = hist_sum1 / hist_count1
        avg_hist2 = hist_sum2 / hist_count2
        avg_hist1[hist_count1 == 0] = np.nan
        avg_hist2[hist_count2 == 0] = np.nan

    # Subtract histograms where both have valid values
    with np.errstate(invalid='ignore'):
        diff_hist = avg_hist1 - avg_hist2
        diff_hist[np.isnan(avg_hist1) | np.isnan(avg_hist2)] = np.nan

    # Subtract histograms where both have valid (non-NaN) values
    with np.errstate(invalid='ignore'):
        diff_hist = avg_hist1 - avg_hist2
        diff_hist[np.isnan(avg_hist1) | np.isnan(avg_hist2)] = np.nan

    return diff_hist, common_edges
