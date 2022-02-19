

from pyrobot.camera.aruco import ArucoDetector
from pyrobot.camera.utils import load_image, save_image


marker_detector = ArucoDetector()


image = load_image("tests/data/aruco.jpg")

what = marker_detector.detect(image)


marker_detector.estimate_pose(image)