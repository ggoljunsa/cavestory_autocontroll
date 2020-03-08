import cv2
import numpy as np
from PIL import ImageGrab

# for keyborad configuration
import pyautogui as pg
import time as t

window_x = 0
window_y = 50
window_w = 700
widow_h = 600

print("start in 2 seconds")
t.sleep(2)

tracker = cv2.TrackerCSRT_create()

img_original = ImageGrab.grab(
    bbox=(window_x, window_y, window_w, widow_h)
)  # x, y, w, h

img_np = np.array(img_original)
img_color = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

cv2.namedWindow("SelectWindow")
cv2.imshow("SelectWindow", img_color)

# ROI 구하기
rect = cv2.selectROI("SelectWindow", img_color, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("SelectWindow")

# Tracker 설정하기
tracker.init(img_color, rect)


while True:
    # img_color = cv.imread('C:/Users/COM-11/Documents/hsv.jpg')
    img_original = ImageGrab.grab(
        bbox=(window_x, window_y, window_w, widow_h)
    )  # x, y, w, h
    img_np = np.array(img_original)
    img_color = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    sucess, box = tracker.update(img_color)

    left, top, w, h = [int(v) for v in box]

    cv2.rectangle(
        img_color,
        pt1=(left, top),
        pt2=(left + w, top + h),
        color=(255, 255, 255),
        thickness=3,
    )

    cv2.imshow("img_color", img_color)

    k = cv2.waitKey(5)
    if k == ord("q"):
        break

cv2.destroyAllWindows()
