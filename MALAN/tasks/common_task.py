import random, time
from datetime import datetime, timedelta

import mss
import pyautogui as pag
from pynput.keyboard import Key


sct = mss.mss()


class ChannelChangeTask:
    def __init__(self):
        pass

    def run(self, runner):
        # self.do_normal(runner)
        self.do_special(runner)
    
    def do_normal(self, runner):
        nx = 700 + 140 * 6       # ※※채널 x방향 n번째 ※※
        ny = 482 + 42 * 10  # ※※채널 y방향 n번째 ※※
        while not runner.stop_controller.is_stopped():
            rx = random.randrange(0, 80)
            ry = random.randrange(0, 21)
            
            runner.move_mouse(1410+rx, 1340+ry, 0.05)      #메뉴
            runner.click(wait=0.155)
            
            runner.tap(Key.enter, 0.45)
            # runner.move_mouse(1380+rx, 1045+ry, 0.05)    #채널변경
            # runner.click(wait=0.25)

            runner.move_mouse(nx+rx, ny+ry, 0)    # ※※채널※※
            runner.click()
            
            runner.tap(Key.enter, 0.1)
            runner.tap(Key.esc, 0.1)


    def do_special(self, runner):
        monitor = {"left": 950, "top": 550, "width": 1, "height": 1}
        while not runner.stop_controller.is_stopped():
            runner.tap(Key.esc, 0.1)
            runner.tap(Key.enter, 0.4)
            runner.tap(Key.right, 0.2)
            img = sct.grab(monitor)
            color = img.pixel(0, 0)  # (R, G, B)
            if color == (221, 221, 221):
                runner.tap(Key.enter, 0.1)
                print("채널찾기종료")
                break
                # runner.tap(Key.esc, 0.5)
            else:
                runner.tap(Key.esc, 0.2)
        if color == (238, 238, 238):
            pass


class NotebookChannelChangeTask:
    def __init__(self):
        pass

    def run(self, runner):
        nx = 400 + 135 * 4       # ※※채널 x방향 n번째 ※※
        ny = 200 + 45 * 10  # ※※채널 y방향 n번째 ※※
        while not runner.stop_controller.is_stopped():
            rx = random.randrange(0, 70)
            ry = random.randrange(0, 11)
            runner.move_mouse(1270+rx, 1020+ry, 0.05)      #메뉴
            runner.click(wait=0.16)
            runner.move_mouse(1270+rx, 740+ry, 0.05)    #채널변경
            runner.click(wait=0.4)
            # runner.move_mouse(1768, 855, 0.01)        #아래 스크롤
            # runner.click()
            runner.move_mouse(nx+rx, ny+ry, 0)    # ※※채널※※
            runner.click()
            runner.tap(Key.enter, 0.01)
            runner.tap(Key.esc, 0.16)


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
                runner.move_mouse(x, y, 0.1)
                runner.click(wait=0.15)
                runner.move_mouse(package_x, package_y, 0.04)
                runner.click(wait=0.15)
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
                x, y = pag.locateCenterOnScreen("../imgs/cider.png", confidence=0.8, region=(1200, 40, 800, 1040))
                package_x = pack_stand_x + 15  + (i%6)*53
                package_y = pack_stand_y - 95 + (i//6)*55
                runner.move_mouse(x, y, 0.04)
                runner.click(wait=0.2)
                runner.move_mouse(package_x, package_y, 0.04)
                runner.click(wait=0.2)
            except pag.ImageNotFoundException as e:
                print(e)
                break


class CharliTask:
    def __init__(self):
        pass

    def run(self, runner):
        try:
            charli_x, charli_y = pag.locateCenterOnScreen("../imgs/charli.png", confidence=0.7)
            charli_y -= 20
            for _ in range(18):
                runner.move_mouse(charli_x, charli_y, 0.1)
                runner.click(wait=0.15) # 찰리 클릭
                
                runner.move_mouse(1700, 770, 0.1)
                runner.click(wait=0.15) # 다음 클릭

                runner.move_mouse(1650, 870, 0.1)
                runner.click(wait=0.15) # 예 클릭

                # for _ in range(60):
                #     runner.scroll(dy=-1, wait=0.02)
                runner.mouse_drag(1760, 470, 1763, 953)
                time.sleep(0.2)

                # runner.move_mouse(1100, 450, 0.1) # 헥터
                runner.move_mouse(1100, 560, 0.1) # 화팽
                runner.click(wait=0.15) # 예 클릭

                runner.move_mouse(1650, 870, 0.1)
                runner.click(wait=0.15) # 예 클릭

                runner.move_mouse(1700, 770, 0.1)
                runner.click(wait=0.15) # 다음 클릭
            
        except pag.ImageNotFoundException as e:
            print(e)
            

class FlJumpTask:
    def __init__(self):
        pass

    def run(self, runner):
        runner.press(Key.right, 0.04)
        runner.press(Key.space, 0.04)
        runner.release(Key.space, 0.03)
        runner.release(Key.right, 0.03)

        runner.press(Key.left, 0.04)
        runner.press("x", 0.02)
        runner.release("x", 0.06)
        runner.release(Key.left, 0.04)

