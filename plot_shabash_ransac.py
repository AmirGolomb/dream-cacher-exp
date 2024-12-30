import matplotlib.pyplot as plt
import yaml
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_3d_data(final_locations, shabash_loc_2d_and_zs, shabash_loc_3d, ransac_line_point, ransac_direction_vector ):
    """
    Plot the 3D points, the fitted line, and the plane z=77.

    Parameters:
    - final_locations (array-like): List or array of final 3D points to plot.
    - shabash_loc_2d_and_zs (array-like): List or array of 3D points to plot with purple X's.
    - shabash_loc_3d (array-like): A single 3D point to plot with a red X.
    - coef (array): Coefficients of the fitted line [coef_x, coef_y].
    - intercept (float): Intercept of the fitted line.
    """
    # Create a figure and 3D axis
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    # Plot final_locations (transparent gray)
    final_locations_array = np.array(final_locations)
    ax.scatter(final_locations_array[:, 0], final_locations_array[:, 1], final_locations_array[:, 2],
               color=(0.5, 0.5, 0.5, 0.3), label="Final Locations", s=50)

    # Plot shabash_loc_2d_and_zs (purple X's)
    shabash_loc_2d_and_zs_array = np.array(shabash_loc_2d_and_zs)
    ax.scatter(shabash_loc_2d_and_zs_array[:, 0], shabash_loc_2d_and_zs_array[:, 1], shabash_loc_2d_and_zs_array[:, 2],
               color='purple', marker='x', s=100, label="Shabash 2D & Zs")

    # Plot shabash_loc_3d (red X)
    print(f'shabash_loc_3d={shabash_loc_3d}')
    ax.scatter(shabash_loc_3d[0], shabash_loc_3d[1], shabash_loc_3d[2],
               color='red', marker='x', s=200, label="Theo Shabash 3D")

    # Plot shabash_loc_3d (red X)
    with open('csv_lines_config.yaml', 'r') as file:
        data = yaml.safe_load(file)
        config = data[data['config']]
    real_shabash_loc = config["real_shabash_loc"]
    print(f'real_shabash_loc={real_shabash_loc}')
    ax.scatter(real_shabash_loc[0], real_shabash_loc[1], real_shabash_loc[2],
               color='black', marker='x', s=200, label="Exp Shabash 3D")

    # Plot the 3D line (RANSAC regression)
    # Plot the fitted line
    line_t = np.linspace(-300, 300, 100)  # Parameter range for visualization
    line_x = ransac_line_point[0] + line_t * ransac_direction_vector[0]
    line_y = ransac_line_point[1] + line_t * ransac_direction_vector[1]
    line_z = ransac_line_point[2] + line_t * ransac_direction_vector[2]
    ax.plot(line_x, line_y, line_z, color='red', label='Fitted Line')


    # Plot the horizontal plane z=77
    xx, yy = np.meshgrid(np.linspace(final_locations[:, 0].min(), final_locations[:, 0].max(), 100),
                         np.linspace(final_locations[:, 1].min(), final_locations[:, 1].max(), 100))
    zz = np.full_like(xx, 77)  # z=77 plane

    # Plot the plane
    ax.plot_surface(xx, yy, zz, color='lightblue', alpha=0.3, label="Plane z=77")

    # Labels for axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Add legend
    # ax.legend()

    # Show plot
    plt.show()
