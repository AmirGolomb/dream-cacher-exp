import numpy as np
import matplotlib.pyplot as plt

def find_shabash_2d_bins(x_history, y_history, evodif_history):
    """
    Finds the position of the source by averaging the positions of points where evodif > 60.
    Also plots all points, highlights points with evodif > 60, and marks the source position.

    Parameters:
    - x_history (np.ndarray): Array of x-coordinates of points.
    - y_history (np.ndarray): Array of y-coordinates of points.
    - evodif_history (np.ndarray): Array of evodif values at each point.

    Returns:
    - source_position (tuple): The estimated position of the source as (x, y).
    """
    print(234567)
    # Ensure the inputs are NumPy arrays
    x_history = np.asarray(x_history)
    y_history = np.asarray(y_history)
    evodif_history = np.asarray(evodif_history)

    # Find indices of points where evodif > 60
    high_evodif_indices = evodif_history > 60

    # Extract x and y coordinates of points with evodif > 60
    high_evodif_x = x_history[high_evodif_indices]
    high_evodif_y = y_history[high_evodif_indices]

    # Calculate the average position of these points
    if len(high_evodif_x) > 0 and len(high_evodif_y) > 0:
        source_x = np.mean(high_evodif_x)
        source_y = np.mean(high_evodif_y)
    else:
        return None
        # raise ValueError("No points with evodif > 60 found.")

    source_position = (source_x, source_y)

    # Plot all points
    plt.figure(figsize=(10, 8))
    plt.scatter(x_history, y_history, label="All points", alpha=0.6, color="blue")

    # Highlight points with evodif > 60
    plt.scatter(high_evodif_x, high_evodif_y, label="evodif > 60", alpha=0.8, color="orange")

    # Mark the source position with a red X
    plt.scatter(source_x, source_y, color="red", label="Source Position", marker="x", s=100)

    # Add labels and legend
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Source Estimation from evodif > 60")
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
