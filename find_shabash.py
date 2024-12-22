import numpy as np
import yaml
from scipy.optimize import least_squares

from read_csv import load_data_for_graph


def find_shabash(x_coords, y_coords, z_coords, electric_field_strengths, bounds):
    # List of points in 3D space and their corresponding electric field strengths
    points = np.array([[x_i, y_i, z_i] for x_i, y_i, z_i in zip(x_coords, y_coords, z_coords)])
    E_original = np.array(electric_field_strengths)  # Electric field strengths
    E_normalized = E_original / np.max(E_original)
    # Function to calculate the difference between predicted and actual electric field strengths

    def residuals(params):
        x_s, y_s, z_s, C = params
        predicted_r = np.sqrt((points[:, 0] - x_s)**2 + (points[:, 1] - y_s)**2 + (points[:, 2] - z_s)**2)
        predicted_E = C / predicted_r**2

        return predicted_E - E_normalized

    # Initial guess for the source coordinates (x_s, y_s, z_s) and constant C
    # initial_guess = 0.5 * (np.array(bounds[0]) + np.array(bounds[1]))

    initial_guess = [(lower + upper) / 2 for lower, upper in zip(bounds[0], bounds[1])]
    # print(f'initial_guess={initial_guess}')

    # Solve for the source location and constant C

    result = least_squares(residuals, initial_guess, bounds=bounds)

    x_s, y_s, z_s, C = result.x

    print(f"Source location: ({x_s}, {y_s}, {z_s})")
    print(f"Constant C: {C}")


if __name__ == '__main__':

    bounds = ([90, 90, 99, -1e10], [110, 110, 101, 1e10])


    locations_example = [[101, 99, 100], [100, 100, 105], [100, 100, 100]]
    info_example = [1, 1, 3]
    find_shabash(*locations_example, info_example, bounds)
    print('-------b-------')

    bounds = ([-10, -10, -1, 0], [10, 10, 1, 1e10])

    locations_example = [[1, -1, 0], [0, 0, 5], [0, 0, 0]]
    info_example = [1, 1, 3]
    find_shabash(*locations_example, info_example, bounds)
    print('-------c-------')

    locations_example = [[4, 4, 4], [0, 3, -3], [0, 0, 0]]
    info_example = [1/16, 1/25, 1/25]
    find_shabash(*locations_example, info_example, bounds)

    print('-------d-------')

    with open('csv_lines_config.yaml', 'r') as file:
        data = yaml.safe_load(file)
        config = data[data['config']]


    min = 31.631237024107612, 34.65422047295317
    max = 31.634641889882253, 34.66058655611044
    bounds = ([31.631237024107612, 34.65422047295317, 0, -1e10], [31.634641889882253, 34.66058655611044, 300, 1e10])


    for graph_config in config['graphs']:
        history_location, history_info = load_data_for_graph(config, graph_config)
        find_shabash(*history_location, history_info, bounds)