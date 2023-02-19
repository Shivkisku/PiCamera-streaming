import argparse
import cv2
import zmq

from camera.Camera import Camera
from constants import PORT, SERVER_ADDRESS
from utils import image_to_string

class Streamer:
    def __init__(self, server_address=SERVER_ADDRESS, port=PORT):
        """
        Tries to connect to the StreamViewer with supplied server_address and creates a socket for future use.
        :param server_address: Address of the computer on which the StreamViewer is running, default is `localhost`
        :param port: Port which will be used for sending the stream
        """
        print(f"Connecting to {server_address} at {port}")
        context = zmq.Context()
        self.footage_socket = context.socket(zmq.PUB)
        self.footage_socket.connect(f"tcp://{server_address}:{port}")
        self.keep_running = True

    def start(self):
        """
        Starts sending the stream to the Viewer.
        Creates a camera, takes a image frame converts the frame to string and sends the string across the network
        :return: None
        """
        print("Streaming started...")
        camera = Camera()
        camera.start_capture()
        self.keep_running = True

        while self.keep_running:
            try:
                frame = camera.current_frame.read()  # grab the current frame
                image_as_string = image_to_string(frame)
                self.footage_socket.send(image_as_string)

            except KeyboardInterrupt:
                break

        camera.stop_capture()
        self.footage_socket.close()
        print("Streaming stopped.")

    def stop(self):
        """
        Sets 'keep_running' to False to stop the running loop if running.
        :return: None
        """
        self.keep_running = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="IP address of the server to connect to", required=True)
    parser.add_argument("-p", "--port", help=f"Port for the streaming server, default is {PORT}", required=False)

    args = parser.parse_args()
    server_address = args.server
    port = args.port or PORT

    streamer = Streamer(server_address, port)
    streamer.start()

if __name__ == '__main__':
    main()
