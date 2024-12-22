from itertools import cycle

import numpy as np
from matplotlib import cm
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def kde_layer_clustering(heights):
    heights = np.array(heights)
    # Sort the data and get indices
    sorted_indices = np.argsort(heights)
    heights_sorted = heights[sorted_indices]

    # Fit Kernel Density Estimation
    bandwidth = 5  # Adjust based on your data
    kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth)
    kde.fit(heights_sorted.reshape(-1, 1))

    # Evaluate the density across the range of heights
    x_d = np.linspace(min(heights_sorted), max(heights_sorted), 1000)
    log_density = kde.score_samples(x_d.reshape(-1, 1))

    # Find local minima in the density (splitting points)
    minima_indices = find_peaks(-log_density)[0]
    split_points = x_d[minima_indices]
    print(f'split_points={split_points}')

    # Segment the heights into layers (by indices)
    groups_of_indices = []
    current_group = []

    # Iterate through sorted heights and assign to groups based on split points
    split_idx = 0  # Pointer to the current split point
    for i, height in enumerate(heights_sorted):
        # Check if we've reached a new split point
        if split_idx < len(split_points) and height >= split_points[split_idx]:
            # Save the current group and reset
            groups_of_indices.append(current_group)
            current_group = []
            split_idx += 1  # Move to the next split point

        # Add the current index to the current group
        current_group.append(sorted_indices[i])

    # Append the last group if not empty
    if current_group:
        groups_of_indices.append(current_group)

    # Print the indices of each group
    for i, group in enumerate(groups_of_indices, 1):
        print(f"Group {i}: {group}")

    # Optional: Visualize the KDE and splitting points
    plt.plot(x_d, np.exp(log_density), label="Density")
    print(f'split_points={split_points.shape}')
    # plt.scatter(split_points, np.exp(log_density[minima_indices]), color='red', label='Splits')
    # plt.xlabel("Height")
    # plt.ylabel("Density")
    # plt.legend()
    # plt.title("KDE-Based Clustering")
    # plt.show()
    return [np.array(group) for group in groups_of_indices]


def cluster_and_visualize(history_location):
    """
    Cluster points by their Z-values and visualize each cluster in a different color.

    Args:
        history_location (list of lists): A list of 3 lists [x_values, y_values, z_values].
    """
    x_values, y_values, z_values = history_location

    # Perform clustering on Z values using kde_layer_clustering
    groups_of_indices = kde_layer_clustering(z_values)

    # Prepare the plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Generate unique colors for each cluster
    colors = cycle(cm.tab10.colors)

    # Plot each cluster in a different color
    for group, color in zip(groups_of_indices, colors):
        cluster_x = [x_values[i] for i in group]
        cluster_y = [y_values[i] for i in group]
        cluster_z = [z_values[i] for i in group]

        ax.scatter(cluster_x, cluster_y, cluster_z, color=color, label=f"Cluster {len(group)}")

    # Customize plot
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Clustering by Z Values")
    ax.legend()
    plt.show()


