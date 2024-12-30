import numpy as np


def points_from_histogram(histogram, edges):
    # Create bin centers for each dimension
    bin_centers = [0.5 * (edges[i][1:] + edges[i][:-1]) for i in range(len(edges))]

    # Get the 3D grid of bin centers (cartesian product of all dimensions' centers)
    grid_points = np.array(np.meshgrid(*bin_centers, indexing="ij")).T.reshape(-1, 3)

    # Flatten the diff_hist to match the shape of the grid_points
    values = histogram.flatten()

    # Create a mask for values that are not NaN
    valid_mask = ~np.isnan(values)

    # Apply the mask to both grid_points and values to filter out NaN entries
    filtered_grid_points = grid_points[valid_mask]
    filtered_values = values[valid_mask]

    return filtered_grid_points, filtered_values

def points_from_histogram_avg_loc(histogram, edges, avg_positions_sample1, avg_positions_sample2):

    # Create bin centers for each dimension
    bin_centers = [0.5 * (edges[i][1:] + edges[i][:-1]) for i in range(len(edges))]

    # Get the 3D grid of bin centers (cartesian product of all dimensions' centers)
    grid_points = np.array(np.meshgrid(*bin_centers, indexing="ij")).T.reshape(-1, 3)

    # Flatten the diff_hist to match the shape of the grid_points
    values = histogram.flatten()

    # Create a mask for values that are not NaN
    valid_mask = ~np.isnan(values)

    # Apply the mask to both grid_points and values to filter out NaN entries
    filtered_grid_points = grid_points[valid_mask]
    filtered_values = values[valid_mask]

    # Also filter the average positions for sample1 and sample2 based on the same valid_mask
    filtered_avg_positions_sample1 = avg_positions_sample1[valid_mask]
    filtered_avg_positions_sample2 = avg_positions_sample2[valid_mask]
    average_filtered_positions = (filtered_avg_positions_sample1 + filtered_avg_positions_sample2) / 2

    return filtered_grid_points, average_filtered_positions, filtered_values,
