import cv2
import numpy as np
from PIL import ImageGrab

color_bgr = [144, 165, 53]
pixel = np.uint8([[color_bgr]])
color_hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
color_hsv = color_hsv[0][0]  # 4 214 255

print(color_hsv)
