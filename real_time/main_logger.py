from argparse import ArgumentParser
from queue import Queue
import threading
import cv2
from cv2 import imshow
import yaml

from rssi_graph import RssiGraph
from real_time.location_graph import LocationGraph
from thread_helper import CaptureThread
from thread_helper import TelemetryThread

# based on eyesatop_basic_example

def print_from_telemetry(telemetry_to_print, key_name: str, accuracy=None):
    temp = telemetry_to_print[key_name]
    if temp is None:
        return "N/A"
    if accuracy is None:
        return temp
    return f'{temp:.{accuracy}f}'


if __name__ == '__main__':
    parser = ArgumentParser('python3 example.py')
    parser.add_argument('--video-port', type=int, default=43000, help='The TCP port to listen on for encoded video.')
    parser.add_argument('--telemetry-port', type=int, default=44000, help='The TCP port to listen on for telemetry.')
    parser.add_argument('--telemetry-bufsize', type=int, default=10240,
                        help='The buffer size for a single telemetry message.')
    ns = parser.parse_args()

    # If you've buily opencv with cuvid support, or support for another hardware decoder, specify it here:
    # os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "video_codec;h264_cuvid"

    # Initialize a threading lock to synchronize threads
    lock = threading.Lock()

    closing = False
    capture_queue = Queue(2)
    capture_thread = CaptureThread('tcp://127.0.0.1:{}?listen'.format(ns.video_port), capture_queue, lock)
    telemetry_thread = TelemetryThread(ns.telemetry_port, ns.telemetry_bufsize, lock)

    capture_thread.start()
    telemetry_thread.start()
    timeout = None
    last_frame = capture_queue.get(timeout=timeout)

    with open(f'config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    if config['show_rssi_flag']:
        rssi_graph = RssiGraph()
    location_graph = LocationGraph(config)

    while not closing and not capture_thread.isFinished() :
        current_frame = capture_queue.get(timeout=timeout)
        telemetry = telemetry_thread.getLatestAsDict()
        # if config['show_rssi_flag']:
        #     rssi_graph.update(telemetry)
        # location_graph.update(telemetry)
       
        imshow("EyesAtop example", current_frame)
        if cv2.waitKey(1) == 27:
            closing = True 
        last_frame = current_frame
        
    capture_thread.close()
    telemetry_thread.close()
    capture_thread.join()
    telemetry_thread.join()