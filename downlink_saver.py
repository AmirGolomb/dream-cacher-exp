import csv
import os

from argparse import ArgumentParser
from queue import Queue
import threading
import cv2
from cv2 import imshow

from thread_helper import CaptureThread as CaptureThread
from thread_helper import TelemetryThread as TelemetryThread

if __name__ == '__main__':
    # Define the CSV file path

    parser = ArgumentParser('python3 example.py')
    parser.add_argument('--video-port', type=int, default=43000, help='The TCP port to listen on for encoded video.')
    parser.add_argument('--telemetry-port', type=int, default=44000, help='The TCP port to listen on for telemetry.')
    parser.add_argument('--telemetry-bufsize', type=int, default=10240,
                        help='The buffer size for a single telemetry message.')
    ns = parser.parse_args()
    lock = threading.Lock()

    closing = False
    capture_queue = Queue(2)

    capture_thread = CaptureThread('tcp://127.0.0.1:{}?listen'.format(ns.video_port), capture_queue, lock)
    telemetry_thread = TelemetryThread(ns.telemetry_port, ns.telemetry_bufsize, lock)

    capture_thread.start()
    telemetry_thread.start()
    timeout = None
    last_frame = capture_queue.get(timeout=timeout)



    # Create the 'csvs' subfolder if it doesn't exist
    os.makedirs("csvs", exist_ok=True)

    # Find an available file name in the 'csvs' folder
    base_file_name = "rssi_06_12_2024_15_10"
    file_index = 1
    csv_file_path = os.path.join("csvs", f"{base_file_name}.csv")

    while os.path.exists(csv_file_path):
        file_index += 1
        csv_file_path = os.path.join("csvs", f"{base_file_name}_v{file_index}.csv")

    # Initialize the CSV file and write the header
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["videoNanoTime", "lat", "lon", "aboveSeaLevel", "upLinkPercent",
                                                  "downLinkPercent", "signalInterference"])
        writer.writeheader()


    last_video_nano_time = None
    # Main loop to capture and save telemetry data
    save_rssi_flag = True
    while not closing and not capture_thread.isFinished():
        current_frame = capture_queue.get(timeout=timeout)
        telemetry = telemetry_thread.getLatestAsDict()

        # Skip saving if videoNanoTime is the same as the last one
        if telemetry.get("videoNanoTime") == last_video_nano_time:
            continue  # Skip this iteration
        last_video_nano_time = telemetry.get("videoNanoTime")

        # Save telemetry data to CSV
        with open(csv_file_path, mode='a', newline='') as file:
            if save_rssi_flag:
                fieldnames = ["videoNanoTime", "lat", "lon", "aboveSeaLevel", "upLinkPercent", "downLinkPercent", "signalInterference"]
            else:
                fieldnames = ["videoNanoTime", "lat", "lon", "aboveSeaLevel", "upLinkPercent", "downLinkPercent"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if save_rssi_flag:
                writer.writerow({
                    "videoNanoTime": telemetry.get("videoNanoTime"),
                    "lat": telemetry.get("lat"),
                    "lon": telemetry.get("lon"),
                    "aboveSeaLevel": telemetry.get("aboveSeaLevel"),
                    "upLinkPercent": telemetry.get("upLinkPercent"),
                    "downLinkPercent": telemetry.get("downLinkPercent"),
                    "signalInterference": telemetry.get("signalInterference")
                })
            else:
                writer.writerow({
                    "videoNanoTime": telemetry.get("videoNanoTime"),
                    "lat": telemetry.get("lat"),
                    "lon": telemetry.get("lon"),
                    "aboveSeaLevel": telemetry.get("aboveSeaLevel"),
                    "upLinkPercent": telemetry.get("upLinkPercent"),
                    "downLinkPercent": telemetry.get("downLinkPercent"),
                })

        # Display the current frame
        imshow("EyesAtop example", current_frame)
        if cv2.waitKey(1) == 27:
            closing = True
        
    capture_thread.close()
    telemetry_thread.close()
    capture_thread.join()
    telemetry_thread.join()