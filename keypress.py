# for keyborad configuration
import pyautogui as pg
import time as t
import threading as th

# for capturing configuration
import numpy as np
import cv2
from PIL import ImageGrab

time_count = 0
fb_Maxarmo = 4


def jump():
    pg.keyDown("z")
    t.sleep(1)
    pg.keyUp("z")


def autoMoveRight():
    pg.keyDown("right")
    t.sleep(2)


def shootOnce():
    pg.keyDown("x")
    t.sleep(0.05)
    pg.keyUp("x")
    t.sleep(0.05)


def switchWeapon(direction="right"):
    if direction == "right":
        pg.keyDown("s")
        t.sleep(0.05)
        pg.keyUp("s")


def autoShoot(weapon="normal", armo=30, comboFlag=False, weaponNum=3):
    if comboFlag == True:
        # 가장 먼저 파이어볼로 조진다
        print("combo acvd")
        for _ in range(weaponNum):
            for i in range(armo):
                shootOnce()
            switchWeapon("right")
    elif comboFlag == False:
        if weapon == "normal":
            # print("ploar star autoShoot")
            for i in range(armo):
                shootOnce()
                # print(i)


def autoMoveJet(direction="right"):
    pg.keyDown("z")
    t.sleep(0.05)
    pg.keyUp("z")
    t.sleep(0.05)
    pg.keyDown(direction)
    t.sleep(0.02)
    pg.keyDown("z")
    t.sleep(1.5)
    pg.keyUp(direction)
    pg.keyUp("z")


def autoMove(direction="left"):
    pg.keyDown(direction)


pg.PAUSE = 0

print("2 seconds to start auto controlling")
t.sleep(2)

# autoShoot()

prevTime = 0


class Messenger(th.Thread):
    def setdata(self, num):
        self.num = num

    def run(self):
        global prevTime
        while True:
            # print("while open %d" % self.num)
            if self.num == 1:
                print("move")
                autoMoveRight()
            if prevTime < time_count:
                print("timecont")
                prevTime = time_count
                if self.num == 2:
                    print("shoot")
                    autoShoot()
                elif self.num == 3:
                    print("jump")
                    jump()
            else:
                continue
            if time_count > 9:
                print("ends!")
                break
        pg.keyUp("right")


a = Messenger(name="a")
b = Messenger(name="b")
c = Messenger(name="c")
d = Messenger(name="d")


def startTimer():
    global time_count
    time_count += 1
    print("time : %d" % time_count)
    timer = th.Timer(1, startTimer)
    timer.start()

    if time_count > 10:
        print("stop")
        timer.cancel()


startTimer()


a.setdata(1)  # 1 is for automove
b.setdata(2)
c.setdata(3)
d.setdata(4)

a.start()
b.start()
c.start()
