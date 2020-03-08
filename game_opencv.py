import cv2
import numpy as np
from PIL import ImageGrab

# for keyborad configuration
import pyautogui as pg
import time as t

rect = 1
threshold = 100
h = 180
lower_blue1 = np.array([176, 47, 47])
upper_blue1 = np.array([180, 255, 255])
lower_blue2 = np.array([0, 47, 47])
upper_blue2 = np.array([6, 255, 255])
lower_blue3 = np.array([166, 47, 47])
upper_blue3 = np.array([176, 255, 255])

window_x = 0
window_y = 70
window_w = 640
widow_h = 480


def nothing(x):
    pass


def mouse_callback(event, x, y, flags, param):
    global hsv, lower_blue1, upper_blue1, lower_blue2, upper_blue2, lower_blue3, upper_blue3, threshold

    # 마우스 왼쪽 버튼 누를시 위치에 있는 픽셀값을 읽어와서 HSV로 변환합니다.
    if event == cv2.EVENT_LBUTTONDOWN:
        print(img_color[y, x])
        color = img_color[y, x]

        one_pixel = np.uint8([[color]])
        hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
        hsv = hsv[0][0]

        threshold = cv2.getTrackbarPos("threshold", "img_result")
        # HSV 색공간에서 마우스 클릭으로 얻은 픽셀값과 유사한 필셀값의 범위를 정합니다.
        if hsv[0] < 10:
            print("case1")
            lower_blue1 = np.array([hsv[0] - 10 + 180, threshold, threshold])
            upper_blue1 = np.array([180, 255, 255])
            lower_blue2 = np.array([0, threshold, threshold])
            upper_blue2 = np.array([hsv[0], 255, 255])
            lower_blue3 = np.array([hsv[0], threshold, threshold])
            upper_blue3 = np.array([hsv[0] + 10, 255, 255])
            #     print(i-10+180, 180, 0, i)
            #     print(i, i+10)

        elif hsv[0] > 170:
            print("case2")
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            upper_blue1 = np.array([180, 255, 255])
            lower_blue2 = np.array([0, threshold, threshold])
            upper_blue2 = np.array([hsv[0] + 10 - 180, 255, 255])
            lower_blue3 = np.array([hsv[0] - 10, threshold, threshold])
            upper_blue3 = np.array([hsv[0], 255, 255])
            #     print(i, 180, 0, i+10-180)
            #     print(i-10, i)
        else:
            print("case3")
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            upper_blue1 = np.array([hsv[0] + 10, 255, 255])
            lower_blue2 = np.array([hsv[0] - 10, threshold, threshold])
            upper_blue2 = np.array([hsv[0], 255, 255])
            lower_blue3 = np.array([hsv[0] - 10, threshold, threshold])
            upper_blue3 = np.array([hsv[0], 255, 255])
            #     print(i, i+10)
            #     print(i-10, i)

        print(hsv[0])
        print("@1", lower_blue1, "~", upper_blue1)
        print("@2", lower_blue2, "~", upper_blue2)
        print("@2", lower_blue2, "~", upper_blue2)
        print("@3", lower_blue3, "~", upper_blue3)


def drawRct(rctNum, width, height, img):
    if rctNum == 1:
        cv2.rectangle(img, (0, 0), (int(width / 3), height), (0, 255, 0), 3)
    elif rctNum == 2:
        cv2.rectangle(
            img, (int(width / 3), 0), (int(width / 3 * 2), height), (255, 0, 0), 3
        )
    elif rctNum == 3:
        cv2.rectangle(img, (int(width / 3 * 2), 0), (width, height), (0, 0, 255), 3)
    else:
        return


cv2.namedWindow("img_color")
cv2.setMouseCallback("img_color", mouse_callback)

# 트랙
cv2.namedWindow("img_result")
cv2.createTrackbar("threshold", "img_result", 0, 255, nothing)
cv2.setTrackbarPos("threshold", "img_result", 30)

while True:
    # img_color = cv.imread('C:/Users/COM-11/Documents/hsv.jpg')
    img_original = ImageGrab.grab(
        bbox=(window_x, window_y, window_w, widow_h)
    )  # x, y, w, h
    img_np = np.array(img_original)
    img_color = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    org_height, org_width = 480, 680
    # print(height, width)
    """
    img_color = cv2.resize(
        img_color, (org_width, org_height), interpolation=cv2.INTER_AREA
    )
    """

    # 원본 영상을 HSV 영상으로 변환합니다.
    img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)

    # 범위 값으로 HSV 이미지에서 마스크를 생성합니다.
    img_mask1 = cv2.inRange(img_hsv, lower_blue1, upper_blue1)
    img_mask2 = cv2.inRange(img_hsv, lower_blue2, upper_blue2)
    img_mask3 = cv2.inRange(img_hsv, lower_blue3, upper_blue3)

    img_mask = img_mask1 | img_mask2 | img_mask3

    # 보간법을 사용해서, 마스킹을 진행해 준다
    kernel = np.ones((11, 11), np.uint8)
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel)
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel)

    # 마스크 이미지로 원본 이미지에서 범위값에 해당되는 영상 부분을 획득합니다.
    img_result = cv2.bitwise_and(img_color, img_color, mask=img_mask)

    # 파이썬에서 추적한 물체에 대한 정보를 주는 함수, 이것으로 쉽게 박스를 그릴 수 있다.
    numOfLables, img_label, stats, centroids = cv2.connectedComponentsWithStats(
        img_mask
    )
    for idx, centroid in enumerate(centroids):
        if stats[idx][0] == 0 and stats[idx][1] == 0:
            continue
        if np.any(np.isnan(centroid)):
            continue

        x, y, width, height, area = stats[idx]
        centerX, centerY = int(centroid[0]), int(centroid[1])
        # print(centerX, centerY)

        # tracker를 떠올리자. 전 프레임에 추적했던 위치, 넓이와 이번 위치 넓이의 일치율이 40% 이상이 되면 같은 물체라 판단하자

        if area > 0:
            cv2.circle(img_color, (centerX, centerY), 10, (0, 0, 255), 10)
            cv2.rectangle(img_color, (x, y), (x + width, y + height), (0, 0, 255))
        if centerX < int(org_width / 3):
            drawRct(1, org_width, org_height, img_result)
        elif centerX < int(org_width / 3 * 2):
            drawRct(2, org_width, org_height, img_result)
        else:
            drawRct(3, org_width, org_height, img_result)

    print(numOfLables)

    if numOfLables == 1:
        print(centroids)

    cv2.imshow("img_color", img_color)
    cv2.imshow("img_mask", img_mask)
    cv2.imshow("img_result", img_result)

    k = cv2.waitKey(5)
    if k == ord("q"):
        break

cv2.destroyAllWindows()
