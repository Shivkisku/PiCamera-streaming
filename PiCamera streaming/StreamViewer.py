import argparse
import threading
import time

import cv2
import numpy as np
import zmq

from constants import PORT
from utils import string_to_image


class StreamViewer:
    def __init__(self, port=PORT):
        """
        Binds the computer to a ip address and starts listening for incoming streams.
        :param port: Port which is used for streaming
        """
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.SUB)
        self.footage_socket.bind('tcp://*:' + port)
        self.footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
        self.current_frame = None
        self.keep_running = threading.Event()

    def receive_stream(self, display=True):
        """
        Keeps updating the 'current_frame' attribute with the most recent frame, this can be accessed using 'self.current_frame'
        :param display: boolean, If False no stream output will be displayed.
        :return: None
        """
        while not self.keep_running.is_set():
            try:
                frame = self.footage_socket.recv_string()
                self.current_frame = string_to_image(frame)

                if display:
                    cv2.imshow("Stream", self.current_frame)
                    cv2.waitKey(1)

            except zmq.error.ContextTerminated:
                break
            except Exception as e:
                print(f"Error receiving stream: {e}")
                break
        print("Streaming stopped.")

    def stop(self):
        """
        Stops the infinite loop in 'receive_stream' method.
        :return: None
        """
        self.keep_running.set()


def main():
    parser = argparse.ArgumentParser(description="Receive and display a video stream.")
    parser.add_argument('-p', '--port', type=int, default=PORT, help='The port number to listen on.')
    args = parser.parse_args()

    stream_viewer = StreamViewer(port=args.port)

    display_thread = threading.Thread(target=stream_viewer.receive_stream, args=(True,))
    display_thread
