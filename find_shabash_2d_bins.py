import numpy as np
import matplotlib.pyplot as plt

def find_shabash_2d_bins(x_history, y_history, evodif_history, plot=False):
    """
    Finds the position of the source by averaging the positions of points with evodif in the top 10%.
    Includes all points with evodif equal to or greater than the cutoff value in cases of ties.
    Also plots all points, highlights selected points, and marks the source position.

    Parameters:
    - x_history (np.ndarray): Array of x-coordinates of points.
    - y_history (np.ndarray): Array of y-coordinates of points.
    - evodif_history (np.ndarray): Array of evodif values at each point.

    Returns:
    - source_position (tuple): The estimated position of the source as (x, y).
    """
    # Ensure the inputs are NumPy arrays
    x_history = np.asarray(x_history)
    y_history = np.asarray(y_history)
    evodif_history = np.asarray(evodif_history)
    print(f'evodif_history={np.unique(evodif_history, return_counts=True)}')

    # Determine the cutoff for the top 10% of evodif values
    threshold = np.percentile(evodif_history, 97)

    # Include all points with evodif >= threshold
    # high_evodif_indices = evodif_history >= threshold
    high_evodif_indices = evodif_history >= 70

    # Extract x and y coordinates of selected points
    high_evodif_x = x_history[high_evodif_indices]
    high_evodif_y = y_history[high_evodif_indices]

    source_position = None
    # Calculate the average position of these points
    if len(high_evodif_x) > 0 and len(high_evodif_y) > 0:
        source_x = np.mean(high_evodif_x)
        source_y = np.mean(high_evodif_y)
        source_position = (source_x, source_y)
    # else:
    #     raise ValueError("No points found in the top 10% of evodif values.")



    if plot:
        # Plot all points
        plt.figure(figsize=(10, 8))
        plt.scatter(x_history, y_history, label="All points", alpha=0.6, color="blue")

        # Highlight points with evodif >= threshold
        plt.scatter(high_evodif_x, high_evodif_y, label=f"Top 10% (diff >= {threshold:.2f})", alpha=0.8, color="orange")

        # Mark the source position with a red X
        plt.scatter(source_x, source_y, color="red", label="Source Position", marker="x", s=100)

        # Add labels and legend
        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.title("Source Estimation from Top 10% evodif")
        plt.legend()
        plt.grid(True)

        # Show the plot
        plt.show()

    return source_position

# Example usage
# x_history = np.array([...])
# y_history = np.array([...])
# evodif_history = np.array([...])
# source_position = find_shabash_2d_bins(x_history, y_history, evodif_history)
# print("Estimated Source Position:", source_position)
