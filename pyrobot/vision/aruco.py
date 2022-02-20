import cv2
import numpy as np
from pprint import pprint



class ArucoDetector:

    def __init__(self):
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
        self.aruco_params = cv2.aruco.DetectorParameters_create()


        self.aruco_params.adaptiveThreshWinSizeMin = 40
        self.aruco_params.adaptiveThreshWinSizeMax = 200
        # aruco_params.minDistanceToBorder =  7
        # aruco_params.cornerRefinementMaxIterations = 149
        # aruco_params.minOtsuStdDev= 4.0

        # aruco_params.minMarkerDistanceRate= 0.014971725679291437
        # aruco_params.maxMarkerPerimeterRate= 10.075976700411534
        # aruco_params.minMarkerPerimeterRate= 0.2524866841549599
        # aruco_params.polygonalApproxAccuracyRate= 0.05562707541937206
        # aruco_params.cornerRefinementWinSize= 9
        # aruco_params.adaptiveThreshConstant= 9.0
        # aruco_params.adaptiveThreshWinSizeMax= 369
        # aruco_params.minCornerDistanceRate= 0.09167132584946237

        self.cam_matrice = np.loadtxt("config/camera_matrice.txt")
        self.cam_distortion = np.loadtxt("config/camera_distortion.txt")

        pprint(self.cam_matrice)
        pprint(self.cam_distortion)

        self.marker_size_cm = 3

    def detect(self, image):
        corners, ids, rejected = cv2.aruco.detectMarkers(
            image, self.aruco_dict, parameters=self.aruco_params,
            cameraMatrix=self.cam_matrice, distCoeff=self.cam_distortion
        )
        print("found", len(corners))
        return corners, ids, rejected

    def draw(self):
        pass
        # cv2.aruco.drawDetectedMarkers(image, corners, ids)

    def estimate_pose(self, image):
        corners, ids, rejected = self.detect(image)


        rot, trans, *args = cv2.aruco.estimatePoseSingleMarkers(
            corners,
            self.marker_size_cm,
            self.cam_matrice,
            self.cam_distortion
        )
        pprint(rot)
        pprint(trans)
        pprint(args)
    