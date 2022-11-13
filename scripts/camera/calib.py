import cv2
from pathlib import Path
import numpy as np
from pprint import pprint

img_paths = list(Path("camera_calib").glob("*.jpg"))


aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
aruco_params = cv2.aruco.DetectorParameters_create()


aruco_params.adaptiveThreshWinSizeMin = 40
aruco_params.adaptiveThreshWinSizeMax = 200
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


print(aruco_params)

allCornersConcatenated = []
allIdsConcatenated = []
markerCounterPerFrame = []
for img_path in img_paths:
    print(img_path)
    image = cv2.imread(str(img_path))

    (corners, ids, rejected) = cv2.aruco.detectMarkers(
        image, aruco_dict, parameters=aruco_params
    )

    print("found", len(corners))

    cv2.aruco.drawDetectedMarkers(image, corners, ids)

    cv2.imwrite(str(Path("output", f"marker_{img_path.name}")), image)

    allCornersConcatenated.extend(corners)
    allIdsConcatenated.extend(ids)
    markerCounterPerFrame.append(len(corners))

    print(image.shape)


allIdsConcatenated = np.array(allIdsConcatenated).squeeze()
markerCounterPerFrame = np.array(markerCounterPerFrame)

# Make Grid
markersX = 5
markersY = 7
markerLength = 10
markerSeparation = 4
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
firstMarker = 0

board = cv2.aruco.GridBoard_create(
    markersX,
    markersY,
    markerLength,
    markerSeparation,
    aruco_dict,
    firstMarker,
)


imsize = (2465, 3280)

cameraMatrixInit = np.array(
    [[1000.0, 0.0, imsize[0] / 2.0], [0.0, 1000.0, imsize[1] / 2.0], [0.0, 0.0, 1.0]]
)
distCoeffsInit = np.zeros((5, 1))

# (ret, camera_matrix, distortion_coefficients0,
#  rotation_vectors, translation_vectors,
#  stdDeviationsIntrinsics, stdDeviationsExtrinsics,
#  perViewErrors)

(
    ret,
    camera_mat,
    distortion_coeff,
    rotation_vec,
    translation_vec,
    *args,
) = cv2.aruco.calibrateCameraAruco(
    allCornersConcatenated,
    allIdsConcatenated,
    markerCounterPerFrame,
    board,
    imsize,
    cameraMatrixInit,
    distCoeffsInit,
    # rvecs,
    # tvecs,
    # calibrationFlags,
)

print(ret)
pprint(camera_mat)

np.savetxt("config/camera_matrice.txt", camera_mat, header=f"image size={imsize}")
np.savetxt(
    "config/camera_distortion.txt", distortion_coeff, header=f"image size={imsize}"
)


for img_path in img_paths:
    print(img_path)
    image = cv2.imread(str(img_path))

    img_undist = cv2.undistort(image, camera_mat, distortion_coeff, None)

    cv2.imwrite(str(Path("output", f"undistort_{img_path.name}")), image)
