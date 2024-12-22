import ast
import csv


def load_data_for_graph(config, graph_config):
    history_location = [[], [], []]
    history_info = []
    for file_config in graph_config['files']:
        load_data_from_csv(config, file_config['csv_file_path'], history_location, history_info, file_config['start_row'],
                  file_config['end_row'])  # Load data for the file range
    return history_location, history_info


def load_data_from_csv(config, csv_file_path, history_location, history_info, start_row=None, end_row=None):
    """Load data from a CSV file, selecting rows by range."""

    with open(csv_file_path, mode='r') as csvfile:
        reader = list(csv.DictReader(csvfile))  # Convert to list to enable slicing
        for row in reader[start_row:end_row]:  # Use row slicing
            if row['lat'] and row['lon'] and row['aboveSeaLevel']:  # Ensure no missing data
                if config['data'] == 'downlink':
                    info = float(row['downLinkPercent'])
                    print(f'info={info}')
                elif config['data'] == 'uplink':
                    info = float(row['upLinkPercent'])
                elif config['data'] == 'rssi':
                    data_list = ast.literal_eval(row['signalInterference'])
                    info = max(item['rssi'] for item in data_list)
                    # info = sum(item['rssi'] for item in data_list)/len([item['rssi'] for item in data_list])
                    # print(info)

                if not config["filter_middle_info"] or info <= config['low_info_ceil'] or config["high_info_floor"] <= info:
                    history_location[0].append(float(row['lon']))
                    history_location[1].append(float(row['lat']))
                    history_location[2].append(float(row['aboveSeaLevel']))
                    history_info.append(info)

