import threading
import time
import cv2
import socket
import json
import select
from queue import Queue, Full, Empty
from threading import Thread


class CaptureThread(Thread):
    def __init__(self, uri: str, queue: Queue, lock: threading.Lock):
        super(CaptureThread, self).__init__()
        self.uri = uri
        self.queue = queue
        self.lock = lock
        self.closed = False
        self.finished = False

    def run(self):
        print("starting video capture thread...")
        
        cap = cv2.VideoCapture(self.uri)
        try:
            while cap.isOpened() and not self.closed:
                ret, frame = cap.read()
                if ret:
                    try:
                        # Acquire lock to ensure thread safety when accessing shared resources
                        with self.lock:
                            self.queue.put_nowait(frame)
                    except Full:
                        self.queue.get_nowait()
                        self.queue.put_nowait(frame)
        finally:
            self.finished = True
            cap.release()

    def isFinished(self):
        return self.finished

    def close(self):
        self.closed = True


class TelemetryThread(Thread):
    def __init__(self, port: int, bufsize: int, lock: threading.Lock):
        super(TelemetryThread, self).__init__()
        self.port = port
        self.bufsize = bufsize
        self.lock = lock
        self.closed = False
        self.finished = False
        self.latest_telemetry = None

    def run(self):
        print("starting API thread...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            s.connect(('127.0.0.1', self.port))
            s.setblocking(False)
            while not self.closed:
                # TelemetryThread - Network I/O with GIL management
                with threading.Lock():
                    ready = select.select([s], [], [], 1)
                if ready[0]:
                    try:
                        data, addr = s.recvfrom(self.bufsize)
                        try:
                            # Split the data into multiple JSON objects if necessary
                            objects = data.decode('UTF-8').splitlines()  # Splitting into lines (or a different separator if needed)
                            for obj in objects:
                                temp = json.loads(obj)  # Try to load each object separately
                                if temp.get("messageType") == "telemetry":
                                    with self.lock:  # Ensure safe access to telemetry data
                                        self.latest_telemetry = temp
                        except json.JSONDecodeError as e:
                            print(f"JSON Decode Error: {e}")
                    except ConnectionResetError:
                        print('record ended')
                        exit()
        except ConnectionRefusedError:
            print('record is off, please start it')
            exit()
        finally:
            self.finished = True
            s.close()

    def isFinished(self):
        return self.finished

    def getLatestAsDict(self):
        return self.latest_telemetry.copy()

    def close(self):
        self.closed = True
