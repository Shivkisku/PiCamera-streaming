import unittest
import numpy
from camera.Camera import Camera


class TestCameraImageCapture(unittest.TestCase):

    def test_capture_image_returns_ndarray(self):
        self.assertIsInstance(Camera().capture_image(), numpy.ndarray)

    def test_capture_image_not_null(self):
        self.assertIsNotNone(Camera().capture_image())


class TestCameraVideoStream(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCameraVideoStream, cls).setUpClass()
        cls.camera = Camera()
        cls.camera.start_capture()

    def test_video_stream_returns_ndarray(self):
        self.assertIsInstance(self.camera.current_frame.read(), numpy.ndarray)

    def test_video_stream_not_null(self):
        self.assertIsNotNone(self.camera.current_frame.read())

    @classmethod
    def tearDownClass(cls):
        super(TestCameraVideoStream, cls).tearDownClass()
        cls.camera.stop_capture()


if __name__ == '__main__':
    unittest.main()
