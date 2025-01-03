import ast
import csv
import time

import numpy as np
import yaml

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.colors as mcolors

from find_shabash import find_shabash
from find_shabash_2d import find_shabash_2d
from read_csv import load_data_for_graph
from subtract_histograms import subtraction_histograms
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

    def plot_graph(self):
        """Plot the final graph based on all loaded data."""
        display_histogram(self.info_histogram, self.plot_edges, self.ax, self.axis_labels, self.cmap, self.norm, self.show_shabash, self.shabash_loc)
        self.ax.set_title(self.config['data'])

        self.fig.canvas.draw_idle()
        plt.pause(0.1)  # Ensure the figure is drawn
        plt.show(block=False)  # Show the graph in a non-blocking way

def run():
    with open('csv_lines_config.yaml', 'r') as file:
        data = yaml.safe_load(file)
        config = data[data['config']]

    two_graphs = []
    two_graphs_labels = []
    two_history_locations = []
    two_history_infos = []
    for graph_config in config['graphs']:
        location_graph = LocationGraph(config)  # Create a new graph object for each graph
        location_graph.history_location, location_graph.history_info = load_data_for_graph(config, graph_config)

        two_history_locations.append(location_graph.history_location)
        two_history_infos.append(location_graph.history_info)
        # print(f'location_graph.history_info={location_graph.history_info}')
        # print(f'location_graph.history_location={location_graph.history_location}')
        # print(f'location_graph.history_info={location_graph.history_info}')

        # cluster_and_visualize(location_graph.history_location)
        # height_groupings = kde_layer_clustering(location_graph.history_location[2])
        # print(f'height_groupings={height_groupings}')
        # print('length', [len(g) for g in height_groupings])
        # for grouping in height_groupings:
        #     locs_in_grouping = location_graph.history_location[:, grouping]
        #     infos_in_grouping = location_graph.history_info[grouping]
            # find_shabash_2d(locs_in_grouping[0], locs_in_grouping[1], infos_in_grouping)

        # raw_comm_stregth =
        find_shabash(*location_graph.history_location, location_graph.history_info, config["find_shabash_bounds"])
        location_graph.fig.suptitle(graph_config['title'], fontsize=14)  # Set the graph title
        location_graph.calculate_histogram()

        two_graphs.append(location_graph)
        two_graphs_labels.append(graph_config['title'])
        location_graph.plot_graph()

    diff_history_location = [two_history_locations[0][i]+two_history_locations[1][i] for i in [0, 1, 2]]
    diff_history_info = two_history_infos[0] + [-info for info in two_history_infos[1]]
    find_shabash(*diff_history_location, diff_history_info, config["find_shabash_bounds"])


    difference_graph = LocationGraph(config, is_diff_graph=True, diff_graph_label=f'{two_graphs_labels[0]}-{two_graphs_labels[1]}')
    diff_hist, common_edges = subtraction_histograms(two_graphs[0].history_location, two_graphs[0].history_info, two_graphs[1].history_location, two_graphs[1].history_info, config['histogram_bins_difference_graph'])
    difference_graph.plot_edges = common_edges
    difference_graph.info_histogram = diff_hist

    difference_graph.plot_graph()
    # for location_graph in two_graphs:
    #     location_graph.plot_graph()

    plt.show()  # Keep all graph windows open

run()

# 'shabash_loc': [34.65720, 31.645779, 50]  # Replace with your specific location if needed