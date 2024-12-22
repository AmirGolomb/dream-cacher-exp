import numpy as np
from matplotlib import pyplot as plt  # Compute bin centers from edges


def display_histogram(histogram_results: np.ndarray, edges: np.ndarray, ax: plt.Axes, axis_labels: np.ndarray | list[str], cmap, norm, show_shabash, shabash_loc):
    x_centers = 0.5 * (edges[0][1:] + edges[0][:-1])
    y_centers = 0.5 * (edges[1][1:] + edges[1][:-1])
    z_centers = 0.5 * (edges[2][1:] + edges[2][:-1])

    # Create a 3D meshgrid of the bin centers
    X, Y, Z = np.meshgrid(x_centers, y_centers, z_centers, indexing="ij")

    # Flatten the histogram and the meshgrid arrays
    values = histogram_results.flatten()
    X_flat = X.flatten()
    Y_flat = Y.flatten()
    Z_flat = Z.flatten()

    # Filter out NaN values
    valid = ~np.isnan(values)
    X_valid, Y_valid, Z_valid, values_valid = X_flat[valid], Y_flat[valid], Z_flat[valid], values[valid]

    # Scatter plot
    # Scale point sizes dynamically
    ax.scatter(X_valid, Y_valid, Z_valid, c=cmap(norm(values_valid)), cmap=cmap,  s=50, alpha=0.4)

    # Label the axes
    ax.set_xlabel(axis_labels[0])
    ax.set_ylabel(axis_labels[1])
    ax.set_zlabel(axis_labels[2])

    # show evo:
    if show_shabash:
        ax.plot(shabash_loc[0], shabash_loc[1], shabash_loc[2], 'ro')

