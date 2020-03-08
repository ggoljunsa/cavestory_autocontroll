import cv2
import numpy as np
from PIL import ImageGrab

# for keyborad configuration
import pyautogui as pg
import time as t
import keypress as kp

window_x = 0
window_y = 50
window_w = 700
widow_h = 600

color_enemy = (84, 173, 165)  # hsv
color_bgr = [41, 70, 255]
pixel = np.uint8([[color_bgr]])
color_hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)
color_hsv = color_hsv[0][0]  # 4 214 255

upper_red = (4, 214, 255)
lower_red = (4, 214, 255)
shootFlag = False


x_tot = 0
y_tot = 0
w_tot = 0
h_tot = 0

x_near = 0
y_near = 0

index = 2

print("start in 2 seconds")
t.sleep(2)


def autoMove(x_tot, y_tot, img):

    if x_tot > 350:
        cv2.rectangle(img, (400, 0), (700, 600), (100, 50, 100), thickness=4)
        pg.keyDown("left")
        pg.keyUp("right")
    elif x_tot < 300:
        cv2.rectangle(img, (0, 0), (300, 600), (50, 100, 100), thickness=4)
        pg.keyDown("right")
        pg.keyUp("left")
    else:
        pg.keyDown("right")
        pg.keyUp("left")


def drawRect(maskingImage, colorImage, heroFlag=True):
    global x_tot, y_tot, index
    # 파이썬에서 추적한 물체에 대한 정보를 주는 함수, 이것으로 쉽게 박스를 그릴 수 있다.
    numOfLables, img_label, stats, centroids = cv2.connectedComponentsWithStats(
        maskingImage
    )
    for idx, centroid in enumerate(centroids):

        if stats[idx][0] == 0 and stats[idx][1] == 0:
            continue
        if np.any(np.isnan(centroid)):
            continue

        x, y, width, height, area = stats[idx]
        centerX, centerY = int(centroid[0]), int(centroid[1])
        # print(centerX, centerY)
        if heroFlag:
            if x > 10 and y > 10:
                x_tot += x
                y_tot += y
                index += 1
        else:
            if area > 0:
                cv2.circle(colorImage, (centerX, centerY), 5, (0, 0, 255), 1)
                cv2.rectangle(colorImage, (x, y), (x + width, y + height), (0, 0, 255))

    if heroFlag:
        if index == 0:
            index = 1

        x_tot /= index
        y_tot /= index
        x_tot = int(x_tot)
        y_tot = int(y_tot)
        # print(x_tot, y_tot, w_tot, h_tot)
        cv2.circle(colorImage, (x_tot, y_tot), 3, (255, 0, 0), 2)

        cv2.rectangle(
            colorImage,
            (x_tot - 10, y_tot - 10),
            (x_tot + 10, y_tot + 10),
            (0, 255, 0),
            thickness=1,
        )

        # autoMove(x_tot, y_tot, img_color)


def safeRect(colorImg, weaponRange=450, jumpHeight=300):
    global shootFlag
    distance = abs(x_tot - x_near)
    lv1 = weaponRange
    lv2 = weaponRange / 3 * 2

    if distance <= lv2:
        cv2.rectangle(
            colorImg,
            (x_tot - int(lv2 / 2), y_tot + 40),
            (x_tot + int(lv2 / 2), y_tot - 40),
            (100, 234, 231),
            1,
        )
        shootFlag = True
    elif distance <= lv1:
        cv2.rectangle(
            colorImg,
            (x_tot - int(lv1 / 2), y_tot + 40),
            (x_tot + int(lv1 / 2), y_tot - 40),
            (0, 231, 234),
            1,
        )
        shootFlag = True
    else:
        shootFlag = False
    print(shootFlag)


def vrbRef():
    global x_tot, y_tot, index
    x_tot = 0
    y_tot = 0

    index = 0


def main():

    kp.Messenger(name="a").setdata(2).start()

    while True:
        img_original = ImageGrab.grab(
            bbox=(window_x, window_y, window_w, widow_h)
        )  # x, y, w, h
        img_np = np.array(img_original)
        img_color = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        img_hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)

        img_mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
        img_mask2 = cv2.inRange(img_hsv, color_enemy, color_enemy)
        # definitions
        drawRect(img_mask1, img_color, True)
        drawRect(img_mask2, img_color, False)
        safeRect(img_color)
        vrbRef()

        img_result = cv2.bitwise_and(img_color, img_color, mask=img_mask1)
        # tracker를 떠올리자. 전 프레임에 추적했던 위치, 넓이와 이번 위치 넓이의 일치율이 40% 이상이 되면 같은 물체라 판단하자
        cv2.imshow("img_mask", img_result)
        cv2.imshow("img_color", img_color)

        k = cv2.waitKey(5)
        if k == ord("q"):
            break

    cv2.destroyAllWindows()


main()

