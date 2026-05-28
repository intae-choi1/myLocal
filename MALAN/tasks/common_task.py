import random
from datetime import datetime, timedelta

import pyautogui as pag
from pynput.keyboard import Key


class ChannelChangeTask:
    def __init__(self):
        pass

    def run(self, runner):
        nx = 560 + 170 * 4       # ※※채널 x방향 n번째 ※※
        ny = 250 + 60 * 10  # ※※채널 y방향 n번째 ※※
        while not runner.stop_controller.is_stopped():
            rx = random.randrange(0, 80)
            ry = random.randrange(0, 11)
            runner.move_mouse(1695+rx, 1330+ry, 0.05)      #메뉴
            runner.click(wait=0.06)
            runner.move_mouse(1695+rx, 975+ry, 0.05)    #채널변경
            runner.click(wait=0.2)
            # runner.move_mouse(1768, 855, 0.01)        #아래 스크롤
            # runner.click()
            runner.move_mouse(nx+rx, ny+ry, 0)    # ※※채널※※
            runner.click()
            runner.tap(Key.enter, 0.01)
            runner.tap(Key.esc, 0.06)



class PutCiderTask:
    def __init__(self):
        pass

    def run(self, runner):
        pack_stand_x, pack_stand_y = pag.locateCenterOnScreen("../imgs/meso_post.png", confidence=0.7)
        for i in range(12):
            try:
                x, y = pag.locateCenterOnScreen("../imgs/cider.png", confidence=0.9, region=(880, 40, 1600, 1400))
                package_x = pack_stand_x + 25  + (i%6)*100
                package_y = pack_stand_y - 180 + (i//6)*100
                runner.move_mouse(x, y, 0.04)
                runner.click(wait=0.12)
                runner.move_mouse(package_x, package_y, 0.04)
                runner.click(wait=0.12)
            except pag.ImageNotFoundException as e:
                print(e)
                break


class NotebookPutCiderTask:
    def __init__(self):
        pass

    def run(self, runner):
        pack_stand_x, pack_stand_y = pag.locateCenterOnScreen("../imgs/meso_post.png", confidence=0.7)
        for i in range(12):
            try:
                x, y = pag.locateCenterOnScreen("../imgs/cider.png", confidence=0.9, region=(1200, 40, 800, 1040))
                package_x = pack_stand_x + 15  + (i%6)*53
                package_y = pack_stand_y - 95 + (i//6)*55
                runner.move_mouse(x, y, 0.04)
                runner.click(wait=0.2)
                runner.move_mouse(package_x, package_y, 0.04)
                runner.click(wait=0.2)
            except pag.ImageNotFoundException as e:
                print(e)
                break