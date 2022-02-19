

import cv2
import time
import picamera
import numpy as np

image_size = (640, 480)

with picamera.PiCamera() as camera:
    camera.resolution = image_size
    camera.framerate = 24
    time.sleep(2)
    output = np.empty((*image_size, 3), dtype=np.uint8)
    camera.capture(output, 'rgb')

    print(output.shape)


cv2.imwrite('pict.jpg', output)