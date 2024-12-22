import numpy as np
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Input data
# x_history = np.array([...])  # Replace with your data
# y_history = np.array([...])
# evodif_history = np.array([...])

def find_shabash_2d(x_history, y_history, evodif_history):
    x_history = np.array(x_history)
    y_history = np.array(y_history)
    evodif_history = np.array(evodif_history)
    # Step 1: Create a regular grid for interpolation
    grid_x, grid_y = np.meshgrid(
        np.linspace(x_history.min(), x_history.max(), 100),
        np.linspace(y_history.min(), y_history.max(), 100)
    )

    # Interpolate evodif_history onto the grid
    grid_evodif = griddata((x_history, y_history), evodif_history, (grid_x, grid_y), method='cubic')

    # Smooth the interpolated data to reduce noise
    smoothed_evodif = gaussian_filter(grid_evodif, sigma=2)

    # Step 2: Compute gradients of smoothed data
    grad_y, grad_x = np.gradient(smoothed_evodif, grid_x[0, 1] - grid_x[0, 0], grid_y[1, 0] - grid_y[0, 0])
    # plt.close()
    # Step 3: Visualization
    plt.figure(figsize=(12, 8))

    # Visualize evodif
    plt.subplot(1, 2, 1)
    plt.title("Interpolated and Smoothed evodif")
    plt.contourf(grid_x, grid_y, smoothed_evodif, levels=50, cmap='viridis')
    plt.colorbar(label='evodif')
    plt.scatter(x_history, y_history, c=evodif_history, edgecolor='k', cmap='viridis', s=50)
    plt.xlabel("X")
    plt.ylabel("Y")

    # Visualize gradients
    plt.subplot(1, 2, 2)
    plt.title("Gradients of evodif")
    plt.quiver(grid_x, grid_y, grad_x, grad_y, color='red', scale=50)
    plt.contourf(grid_x, grid_y, smoothed_evodif, levels=50, cmap='viridis', alpha=0.7)
    plt.colorbar(label='evodif')
    plt.scatter(x_history, y_history, c=evodif_history, edgecolor='k', cmap='viridis', s=50)
    plt.xlabel("X")
    plt.ylabel("Y")

    plt.tight_layout()
    plt.show()

    # Step 4: Define the cost function for optimization
    def cost_function(source, x_data, y_data, evodif_data):
        x_s, y_s = source
        total_cost = 0
        for x, y, evodif in zip(x_data, y_data, evodif_data):
            r = np.sqrt((x - x_s)**2 + (y - y_s)**2) + 1e-9  # Distance to source
            predicted_evodif = 1 / r**2  # Inverse-square law
            total_cost += (evodif - predicted_evodif)**2  # Squared difference
        return total_cost

    # Step 5: Optimize the source location
    initial_guess = [np.mean(x_history), np.mean(y_history)]
    result = minimize(cost_function, initial_guess, args=(x_history, y_history, evodif_history))

    source_location = result.x
    print("Estimated source location:", source_location)

    # Visualize the estimated source on the evodif plot
    plt.figure(figsize=(8, 6))
    plt.title("Estimated Source Location")
    plt.contourf(grid_x, grid_y, smoothed_evodif, levels=50, cmap='viridis')
    plt.colorbar(label='evodif')
    plt.scatter(x_history, y_history, c=evodif_history, edgecolor='k', cmap='viridis', s=50)
    plt.scatter(*source_location, color='red', marker='x', s=200, label='Estimated Source')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()
