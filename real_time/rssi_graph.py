import matplotlib
import matplotlib.pyplot as plt
import time  # Add time import to track elapsed time
matplotlib.use('Qt5Agg')  # Try TkAgg, or you can use 'Qt5Agg' or 'Agg'

class RssiGraph:
    def __init__(self,  max_past_data_length=5):
        plt.ion()  # Turn on interactive mode for dynamic updating
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 5), gridspec_kw={'width_ratios': [5, 1, 1]})
        self.ax1, self.ax2, self.ax3 = ax1, ax2, ax3
        self.max_past_data_length = max_past_data_length
        self.previous_rssi = None
        self.previous_uplink = None
        self.previous_downlink = None
        self.history_rssi = []
        self.history_frequencies = []
        self.history_uplink = []
        self.history_downlink = []

    def update(self, telemetry):
        # Extract signal interference data (frequency and RSSI)
        current_signal_interference = telemetry['signalInterference']
        current_frequencies = [entry['frequencyFrom'] for entry in current_signal_interference]
        current_rssi = [entry['rssi'] for entry in current_signal_interference]
        current_uplink = telemetry['upLinkPercent']
        current_downlink = telemetry['downLinkPercent']


        rssi_updated = current_rssi != self.previous_rssi
        uplink_updated = current_uplink != self.previous_uplink
        downlink_updated = current_downlink != self.previous_downlink
        self.previous_rssi = current_rssi
        self.previous_uplink = current_uplink
        self.previous_downlink = current_downlink

        if not (rssi_updated or uplink_updated or downlink_updated):
            return  # Skip if no updates have occurred

        if rssi_updated:
            self.history_rssi.append(current_rssi)
            self.history_frequencies.append(current_frequencies)
            if len(self.history_rssi) > self.max_past_data_length:
                self.history_rssi.pop(0)  # Remove the oldest data if we exceed the limit
                self.history_frequencies.pop(0)
        if uplink_updated:
            self.history_uplink.append(current_uplink)
            if len(self.history_uplink) > self.max_past_data_length:
                self.history_uplink.pop(0)
        if downlink_updated:
            self.history_downlink.append(current_downlink)
            if len(self.history_downlink) > self.max_past_data_length:
                self.history_downlink.pop(0)





        alpha_multiplier = 1 / self.max_past_data_length / 3

        if rssi_updated:
            print(f'current_frequencies={len(current_frequencies)}, {current_frequencies}')
            print(f'current_rssi={len(current_rssi)}, {current_rssi}')
            self.ax1.clear()
            self.ax1.set_xlabel("Frequency (MHz)")
            self.ax1.set_ylabel("RSSI (dBm)")
            self.ax1.set_title("RSSI vs Frequency over Time")
            self.ax1.grid(True)
            for i, past_rssi in enumerate(self.history_rssi):
                alpha = (i+1) * alpha_multiplier
                
                self.ax1.scatter(self.history_frequencies[i], past_rssi, marker='o', color='b', alpha=alpha)
            self.ax1.scatter(current_frequencies, current_rssi, marker='o', color='k')

        if uplink_updated:
            print(f'current_uplink={current_uplink}')
            self.ax2.clear()
            self.ax2.set_ylim(-5, 105)
            self.ax2.set_title("UpLink")
            self.ax2.set_xticks([])
            for i, past_uplink in enumerate(self.history_uplink):
                alpha = i * alpha_multiplier + 0.2
                self.ax2.scatter([0], [past_uplink], marker='o', color='g', alpha=alpha)
            self.ax2.scatter([0], [current_uplink], marker='o', color='k')

        if downlink_updated:
            print(f'current_downlink={current_downlink}')
            self.ax3.clear()
            self.ax3.set_ylim(-5, 105)
            self.ax3.set_title("DownLink")
            self.ax3.set_xticks([])
            
            for i, past_downlink in enumerate(self.history_uplink):
                alpha = i * alpha_multiplier + 0.2
                self.ax3.scatter([0], [past_downlink], marker='o', color='r', alpha=alpha)
            self.ax3.scatter([0], [current_downlink], marker='o', color='k')
        
        plt.draw()
        plt.pause(0.1)