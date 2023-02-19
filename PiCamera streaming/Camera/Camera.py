import time
import cv2
import imutils
from imutils.video import VideoStream
from constants import IS_RASPBERRY_PI, CAMERA_PORT, RESOLUTION_H, RESOLUTION_W
from utils import preview_image

class Camera:

    def __init__(self, height=RESOLUTION_H, width=RESOLUTION_W):
        self.current_frame = None
        self.height = height
        self.width = width

    def start_capture(self, height=None, width=None, usingPiCamera=IS_RASPBERRY_PI):
        resolution = (self.height, self.width)
        if height and width:
            resolution = (height, width)
        self.current_frame = VideoStream(usePiCamera=usingPiCamera,
                                         resolution=resolution,
                                         framerate=32).start()
        time.sleep(2)

    def stop_capture(self):
        print("Stopping Capture")
        self.current_frame.stop()

    def capture_image(self):
        # Number of frames to throw away while the camera adjusts to light levels
        ramp_frames = 30

        camera = cv2.VideoCapture(CAMERA_PORT)
        _, im = camera.read()
        [camera.read() for _ in range(ramp_frames)]
        print("Taking image...")
        _, camera_capture = camera.read()
        del camera
        return camera_capture

    def __del__(self):
        try:
            self.current_frame.release()
        except AttributeError:
            pass


if __name__ == '__main__':
    # Capture and Display Image
    camera = Camera()
    image = camera.capture_image()
    preview_image(image)

    # Stream Video
    camera.start_capture()
    while True:
        frame = camera.current_frame.read()
        if not IS_RASPBERRY_PI:
            frame = imutils.resize(frame, width=RESOLUTION_W)
        cv2.imshow("Camera Stream", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    camera.stop_capture()
    cv2.destroyAllWindows()
