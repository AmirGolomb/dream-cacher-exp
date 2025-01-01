import matplotlib
import matplotlib.pyplot as plt
import time  # Add time import to track elapsed time
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from multi_dim_histogram import multi_dim_histogram
# from display_histogram import display_histogram_3d

matplotlib.use('Qt5Agg')  # Try TkAgg, or you can use 'Qt5Agg' or 'Agg'

class LocationGraph:
    def __init__(self, config):
        plt.ion()  # Turn on interactive mode for dynamic updating
        self.fig = plt.figure(figsize=(10, 5))
        if config['show_uplink_flag']:
            self.uplink_hist_ax = self.fig.add_subplot(1, 2, 1, projection='3d')
        self.downlink_hist_ax = self.fig.add_subplot(1, 2, 2, projection='3d')
        self.axis_labels = ["lon", "lat", "asl"]
        self.cmap = cm.get_cmap('viridis')  # Choose a colormap
        self.norm = mcolors.Normalize(vmin=0, vmax=100)  # Fixed normalization for the range

        # location color bar:
        sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
        sm.set_array([])
        if config['show_uplink_flag']:
            cbar = self.fig.colorbar(sm, ax=[self.uplink_hist_ax, self.downlink_hist_ax], shrink=0.7, aspect=20, location='right')
        else:
            cbar = self.fig.colorbar(sm, ax=[self.downlink_hist_ax], shrink=0.7, aspect=20, location='right')
        cbar.set_label('Values (0-100)')

        self.histogram_bins = config['histogram_bins']

        self.history_uplink = []
        self.history_downlink = []
        self.history_location = [[], [], []]
        self.history_location = [[], [], []]

        self.shabash_loc = config['shabash_loc']
        self.config = config





    def update(self, telemetry):


        current_location = telemetry['lon'], telemetry['lat'], telemetry['aboveSeaLevel']
        current_uplink = telemetry['upLinkPercent']
        current_downlink = telemetry['downLinkPercent']

        if None not in current_location:
            self.history_uplink.append(current_uplink)
            self.history_downlink.append(current_downlink)
            self.history_location[0].append(float(current_location[0]))
            self.history_location[1].append(float(current_location[1]))
            self.history_location[2].append(float(current_location[2]))

        if None not in current_location:
            if self.config['show_uplink_flag']:
                uplink_hist, edges = multi_dim_histogram(self.history_location, self.history_uplink, bins=self.histogram_bins)
                self.uplink_hist_ax.clear()
                # display_histogram_3d(uplink_hist, edges, self.uplink_hist_ax, self.axis_labels, self.cmap, self.norm, self.shabash_loc)
                self.uplink_hist_ax.set_title('uplink')

            downlink_hist, edges = multi_dim_histogram(self.history_location, self.history_downlink, bins=self.histogram_bins)
            self.downlink_hist_ax.clear()
            # display_histogram_3d(downlink_hist, edges, self.downlink_hist_ax, self.axis_labels, self.cmap, self.norm, self.shabash_loc)
            self.downlink_hist_ax.set_title('downlink')

        self.fig.canvas.draw_idle()
        plt.pause(0.1)
