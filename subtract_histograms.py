from typing import Sequence
import numpy as np


def subtraction_histograms(sample1, values1, sample2, values2, bins: Sequence[int]):
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
    ranges = [
        (min(np.min(sample1[i]), np.min(sample2[i])), max(np.max(sample1[i]), np.max(sample2[i])))
        for i in range(3)
    ]

    # Create a single set of bin edges for all datasets
    common_edges = [np.linspace(r[0], r[1], bins[i] + 1) for i, r in enumerate(ranges)]

    # Rebin both datasets
    hist_sum1, _ = np.histogramdd(sample1.T, bins=common_edges, weights=values1)
    hist_count1, _ = np.histogramdd(sample1.T, bins=common_edges)

    hist_sum2, _ = np.histogramdd(sample2.T, bins=common_edges, weights=values2)
    hist_count2, _ = np.histogramdd(sample2.T, bins=common_edges)

    # Calculate average histograms with the common grid
    with np.errstate(divide='ignore', invalid='ignore'):
        avg_hist1 = hist_sum1 / hist_count1
        avg_hist2 = hist_sum2 / hist_count2
        avg_hist1[hist_count1 == 0] = np.nan
        avg_hist2[hist_count2 == 0] = np.nan

    # Subtract histograms where both have valid (non-NaN) values
    with np.errstate(invalid='ignore'):
        diff_hist = avg_hist1 - avg_hist2
        diff_hist[np.isnan(avg_hist1) | np.isnan(avg_hist2)] = np.nan

    return diff_hist, common_edges

def subtraction_histograms_avg_loc(sample1, values1, sample2, values2, bins):
    """
    Compute the difference between two 3D histograms where bins represent average positions of points in 3D space.
    Only include bins where both histograms have valid values.

    Parameters:
        sample1 (list of ndarray): List of x, y, z coordinates for the first set of points.
        values1 (ndarray): Values associated with points in the first set.
        sample2 (list of ndarray): List of x, y, z coordinates for the second set of points.
        values2 (ndarray): Values associated with points in the second set.
        bins (int or Sequence[int]): Number of bins for the histogram in each dimension.

    Returns:
        diff_hist (ndarray): Difference between histograms.
        common_edges (list of ndarray): Bin edges.
        avg_positions_sample1 (ndarray): Average positions of points in sample1 for each bin.
        avg_positions_sample2 (ndarray): Average positions of points in sample2 for each bin.
    """
    # Define a common grid for rebinning based on the range of all points
    ranges = [
        (min(np.min(sample1[i]), np.min(sample2[i])), max(np.max(sample1[i]), np.max(sample2[i])))
        for i in range(3)
    ]

    # Create a single set of bin edges for all datasets
    common_edges = [np.linspace(r[0], r[1], bins[i] + 1) for i, r in enumerate(ranges)]

    # Rebin both datasets
    hist_sum1, _ = np.histogramdd(sample1.T, bins=common_edges, weights=values1)
    hist_count1, _ = np.histogramdd(sample1.T, bins=common_edges)

    hist_sum2, _ = np.histogramdd(sample2.T, bins=common_edges, weights=values2)
    hist_count2, _ = np.histogramdd(sample2.T, bins=common_edges)

    # Calculate the average histograms for both sample1 and sample2
    with np.errstate(divide='ignore', invalid='ignore'):
        avg_hist1 = hist_sum1 / hist_count1
        avg_hist2 = hist_sum2 / hist_count2
        avg_hist1[hist_count1 == 0] = np.nan
        avg_hist2[hist_count2 == 0] = np.nan

    # Subtract histograms where both have valid (non-NaN) values
    with np.errstate(invalid='ignore'):
        diff_hist = avg_hist1 - avg_hist2
        diff_hist[np.isnan(avg_hist1) | np.isnan(avg_hist2)] = np.nan

    return avg_hist1, avg_hist2, diff_hist, common_edges

def average_loc_of_points_per_bin(sample1, sample2, common_edges):
    # Digitize the points in each sample to find the bin indices for each dimension
    bin_indices1 = [
        np.digitize(sample1[i], common_edges[i]) - 1  # Adjust to 0-based indexing
        for i in range(3)
    ]
    bin_indices2 = [
        np.digitize(sample2[i], common_edges[i]) - 1  # Adjust to 0-based indexing
        for i in range(3)
    ]

    # Stack the indices to get a unique bin identifier for each point
    bin_indices1 = np.stack(bin_indices1, axis=-1)
    bin_indices2 = np.stack(bin_indices2, axis=-1)

    # Create a dictionary to store points in each bin for sample1 and sample2
    from collections import defaultdict

    points_in_bins1 = defaultdict(list)
    points_in_bins2 = defaultdict(list)

    # Fill the dictionary for sample1
    for point, bin_idx in zip(sample1.T, bin_indices1):
        points_in_bins1[tuple(bin_idx)].append(point)

    # Fill the dictionary for sample2
    for point, bin_idx in zip(sample2.T, bin_indices2):
        points_in_bins2[tuple(bin_idx)].append(point)

    # Convert lists to numpy arrays for easier manipulation
    points_in_bins1 = {k: np.array(v) for k, v in points_in_bins1.items()}
    points_in_bins2 = {k: np.array(v) for k, v in points_in_bins2.items()}

    # To calculate the average location of points in each bin:
    average_locations1 = {k: np.mean(v, axis=0) for k, v in points_in_bins1.items()}
    average_locations2 = {k: np.mean(v, axis=0) for k, v in points_in_bins2.items()}

    return average_locations1, average_locations2


def average_loc_and_corresponding_dif(average_locations1, average_locations2, avg_value_hist1, avg_value_hist2):
    # Create lists to store final averaged locations and corresponding values
    final_locations = []
    final_values = []

    # Iterate over all possible bins in average_locations1 and average_locations2
    for bin_idx in average_locations1.keys():
        loc1 = average_locations1.get(bin_idx, None)
        loc2 = average_locations2.get(bin_idx, None)
        val1 = avg_value_hist1[tuple(bin_idx)] if np.all(bin_idx < np.array(avg_value_hist1.shape)) else np.nan
        val2 = avg_value_hist2[tuple(bin_idx)] if np.all(bin_idx < np.array(avg_value_hist2.shape)) else np.nan

        # Check if both locations and both values are valid (not NaN)
        if loc1 is not None and not np.isnan(loc1).any() and \
                loc2 is not None and not np.isnan(loc2).any() and \
                not np.isnan(val1) and not np.isnan(val2):
            # Calculate the average location
            avg_location = (loc1 + loc2) / 2
            # Calculate the value difference
            value_diff = val1 - val2

            # Append to the lists
            final_locations.append(avg_location)
            final_values.append(value_diff)

    # Convert lists to numpy arrays
    final_locations = np.array(final_locations)
    final_values = np.array(final_values)

    # Sanity check: Ensure lengths of final_locations and final_values match
    if len(final_locations) != len(final_values):
        raise ValueError("Mismatch between lengths of final locations and final values!")

    return final_locations, final_values


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_3d_locations_with_values(final_locations, final_values, cmap='viridis'):
    """
    Plots 3D locations with their corresponding values as colors.

    Parameters:
        final_locations (np.ndarray): A numpy array of shape (N, 3) representing 3D points.
        final_values (np.ndarray): A numpy array of shape (N,) representing values corresponding to each point.
        cmap (str): Matplotlib colormap for coloring the points based on final_values.

    Raises:
        ValueError: If final_locations and final_values have mismatched lengths or invalid shapes.
    """
    # Validate input shapes
    if len(final_locations) != len(final_values):
        raise ValueError("final_locations and final_values must have the same length.")
    if final_locations.shape[1] != 3:
        raise ValueError("final_locations must have shape (N, 3).")
    if final_values.ndim != 1:
        raise ValueError("final_values must be a 1D array.")

    # Create 3D scatter plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Normalize final_values for coloring
    norm = plt.Normalize(vmin=np.min(final_values), vmax=np.max(final_values))
    colors = plt.cm.get_cmap(cmap)(norm(final_values))

    # Scatter plot
    sc = ax.scatter(
        final_locations[:, 0],
        final_locations[:, 1],
        final_locations[:, 2],
        c=final_values,
        cmap=cmap,
        s=50,
        edgecolor='k'
    )

    # Add a colorbar
    cbar = fig.colorbar(sc, ax=ax, shrink=0.6)
    cbar.set_label("Value Difference")

    # Labels and title
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_zlabel("Z Coordinate")
    ax.set_title("3D Locations Colored by Value Differences")

    # Show plot
    plt.show()

