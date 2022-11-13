import cv2


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


img_grid = cv2.aruco_GridBoard.draw(
    board,
    (1600, 2000),
    300,  #    marginSize = 0,
    10,  # int  	borderBits = 1
)
print(img_grid.shape)
cv2.imwrite("aruco_grid.png", cv2.cvtColor(img_grid, cv2.COLOR_RGB2BGR))
