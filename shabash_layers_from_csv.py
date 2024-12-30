import ast
import csv
import time

import numpy as np
import yaml

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcolors

from custom_ransac import custom_ransac
from find_shabash import find_shabash
from find_shabash_2d import find_shabash_2d
from find_shabash_2d_bins import find_shabash_2d_bins
from plot_shabash_ransac import plot_3d_data
from points_from_histogram_3d import points_from_histogram, points_from_histogram_avg_loc
from ransac_find_shabash import ransac_find_shabash
from read_csv import load_data_for_graph
from separate_layers import group_heights_by_count, draw_groups_in_3d
from subtract_histograms import subtraction_histograms, subtraction_histograms_avg_loc, average_loc_of_points_per_bin, \
    average_loc_and_corresponding_dif, plot_3d_locations_with_values
from multi_dim_histogram import multi_dim_histogram
from display_histogram import display_histogram


class LocationGraph:
    def __init__(self, config, is_diff_graph=False, diff_graph_label=None):
        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(1, 1, 1, projection='3d')
        self.axis_labels = ["lon", "lat", "asl"]
        self.cmap = cm.get_cmap('viridis')
        self.bar_range = [0, 100] if config["data"] != "rssi" else [-110, -40]
        if is_diff_graph:
            self.cmap = cm.get_cmap('RdYlGn')
            # self.cmap = cm.get_cmap('hsv')
            self.bar_range = [-50, 50]
        self.norm = mcolors.Normalize(vmin=self.bar_range[0], vmax=self.bar_range[1])  # Fixed normalization for the range

        self.show_shabash = config['show_shabash']
        self.shabash_loc = config['shabash_loc']
        self.high_info_floor = config['high_info_floor']
        self.low_info_ceil = config['low_info_ceil']
        self.histogram_bins = config['histogram_bins']
        self.config = config

        self.history_location = [[], [], []]  # lon, lat, asl
        self.history_info = []
        self.plot_edges = None
        self.info_histogram = None

        # Add color bar
        sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
        sm.set_array([])
        cbar = self.fig.colorbar(sm, ax=[self.ax], shrink=0.7, aspect=20, location='right')
        cbar.set_label(f'Values')
        if diff_graph_label is not None:
            cbar.set_label(diff_graph_label)

    def calculate_histogram(self):
        print(f'self.history_location={self.history_location}')
        self.info_histogram, self.plot_edges = multi_dim_histogram(self.history_location, self.history_info, bins=self.histogram_bins)

def plot_diffrence_histogram(info_histogram, plot_edges):
    """Plot the final graph based on all loaded data."""
    ax = plt.figure().add_subplot(projection='3d')
    axis_labels = ["lon", "lat", "asl"]
    cmap = cm.get_cmap('RdYlGn')
    with open('csv_lines_config.yaml', 'r') as file:
        data = yaml.safe_load(file)
        config = data[data['config']]
    show_shabash = config['show_shabash']
    shabash_loc = config['shabash_loc']
    bar_range = [-50, 50]
    norm = mcolors.Normalize(vmin=bar_range[0], vmax=bar_range[1])  # Fixed normalization for the range
    display_histogram(info_histogram, plot_edges, ax, axis_labels, cmap, norm, show_shabash, shabash_loc )
    # ax.set_title(self.config['data'])

    # self.fig.canvas.draw_idle()
    plt.pause(0.1)  # Ensure the figure is drawn
    plt.show(block=False)  # Show the graph in a non-blocking way

def run():
    with open('csv_lines_config.yaml', 'r') as file:
        data = yaml.safe_load(file)
        config = data[data['config']]

    two_graphs_labels = []
    two_history_locations = []
    two_history_infos = []
    for graph_config in config['graphs']:
        # location_graph = LocationGraph(config)  # Create a new graph object for each graph
        history_location, history_info = load_data_for_graph(config, graph_config)
        two_history_locations.append(history_location)
        two_history_infos.append(history_info)
        # _, height_groupings = group_heights_by_count(history_location[2])
        #
        #
        #
        # draw_groups_in_3d(history_location, height_groupings)

        # for grouping in height_groupings:
        #     # print(f'grouping={grouping}')
        #     locs_in_grouping = history_location[:, grouping]
        #     infos_in_grouping = history_info[grouping]
        #     # find_shabash_2d(locs_in_grouping[0], locs_in_grouping[1], infos_in_grouping)
        #     find_shabash_2d_bins(locs_in_grouping[0], locs_in_grouping[1], infos_in_grouping)

    # diff_hist, common_edges = subtraction_histograms(two_history_locations[0], two_history_infos[0],
    #                                                  two_history_locations[1], two_history_infos[1],
    #                                                  config['histogram_bins_difference_graph'])
    avg_value_hist1, avg_value_hist2, diff_hist, common_edges = subtraction_histograms_avg_loc(two_history_locations[0], two_history_infos[0],
                                                     two_history_locations[1], two_history_infos[1],
                                                     config['histogram_bins_difference_graph'])
    average_locations1, average_locations2 = average_loc_of_points_per_bin(two_history_locations[0], two_history_locations[1], common_edges)
    final_locations, final_values = average_loc_and_corresponding_dif(average_locations1, average_locations2, avg_value_hist1, avg_value_hist2)
    # print(f'final_locations={average_locations1}')
    # print(f'final_values={final_values}')
    # Analyze final_values
    num_above_zero = np.sum(final_values > 0)  # Count values above 0
    num_below_zero = np.sum(final_values < 0)  # Count values below 0
    average_value = np.mean(final_values)  # Calculate the average

    print(f"Number of values above 0: {num_above_zero}")
    print(f"Number of values below 0: {num_below_zero}")
    print(f"Average of final_values: {average_value:.2f}")
    final_locations_trans = final_locations.T
    # plot_3d_locations_with_values(final_locations, final_values)
    _, height_groupings = group_heights_by_count(final_locations_trans[2])
    draw_groups_in_3d(final_locations_trans, height_groupings)
    shabash_loc_2d_and_zs = []
    for grouping in height_groupings:
        locs_in_grouping = final_locations_trans[:, grouping]
        # print(f'locs_in_grouping+{locs_in_grouping}')
        grouping_z = np.mean(locs_in_grouping[2])
        infos_in_grouping = final_values[grouping]
        # find_shabash_2d(locs_in_grouping[0], locs_in_grouping[1], infos_in_grouping)
        shabash_loc_2d = find_shabash_2d_bins(locs_in_grouping[0], locs_in_grouping[1], infos_in_grouping, plot=False)

        shabash_loc_2d_and_zs.append((shabash_loc_2d[0], shabash_loc_2d[1], grouping_z))

    # shabash_loc_3d, ransac_coef, ransac_intercept = ransac_find_shabash(shabash_loc_2d_and_zs, ground_asl=77)
    shabash_loc_3d, ransac_line_point, ransac_direction_vector = custom_ransac(shabash_loc_2d_and_zs, ground_asl=77)
    plot_3d_data(final_locations, shabash_loc_2d_and_zs, shabash_loc_3d, ransac_line_point, ransac_direction_vector)

    # plot_diffrence_histogram(diff_hist, common_edges)
    # diff_points, diff_values = points_from_histogram(diff_hist, common_edges)
    # diff_points, diff_values = points_from_histogram_avg_loc(diff_hist, common_edges)
    # print(f'diff_values={np.unique(diff_values, return_counts=True)}')
    # _, height_groupings = group_heights_by_count(diff_points[:, 2])
    # draw_groups_in_3d(diff_points.T, height_groupings)
    plt.show()  # Keep all graph windows open

run()
